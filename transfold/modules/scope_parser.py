# Author: Filip Hajdyła
# Date of creation: 16/11/2023
# Description: Parser functions to get GeneID from PDB ID,
#              and category from SCOPe file

import logging
from pathlib import Path

import pandas as pd
import requests as rq


def get_scope_df(
    scope_path: Path, pattern: str, logger: logging.Logger
) -> pd.DataFrame:
    logger.info(f"Reading SCOPe file: {scope_path}")
    scope_df = pd.read_table(
        scope_path,
        sep="\t",
        header=None,
        names=[
            "scope_id",
            "pdb_id",
            "chain",
            "category",
            "NA1",
            "NA2",
        ],
    )
    logger.info(f"Filtering SCOPe file by category pattern: {pattern}")
    scope_df = scope_df[
        scope_df["category"].str.contains(
            pattern,
            regex=True,
            na=False,
        )
    ]
    return scope_df


def get_pdb_ids(scope_df: pd.DataFrame, logger: logging.Logger) -> list[str]:
    logger.info("Getting unique PDB IDs from SCOPe file")
    return scope_df["pdb_id"].unique().tolist()


def get_category(
    scope_df: pd.DataFrame, pdb_id: str, logger: logging.Logger
) -> str:
    try:
        cat = scope_df[scope_df["pdb_id"] == pdb_id]["category"].tolist()[0]
        logger.debug(f"Category for {pdb_id}: {cat}")
        return cat
    except (KeyError, IndexError):
        logger.error(f"Category for {pdb_id} not found")
        return ""


def get_uniprot_id(
    pdb_id: str, retries: int, timeout: int, logger: logging.Logger
) -> str:
    for _ in range(retries):
        try:
            response = rq.get(
                "https://data.rcsb.org/rest/"
                f"v1/core/polymer_entity/{pdb_id}/1",
                timeout=timeout,
            )
        except Exception:  # pragma: no cover
            logger.warning("Connection timeout. Retrying...")
            continue
        if response.status_code == 200:
            logger.debug("Connected to PDB")
            content = response.json()
            response.close()
            try:
                uniprot_id = content[
                    "rcsb_polymer_entity_container_identifiers"
                ]["uniprot_ids"][0]
                logger.debug(f"Found UniProt ID for {pdb_id}: {uniprot_id}")
            except KeyError:  # pragma: no cover
                logger.error(f"UniProt ID for {pdb_id} not found")
                return ""
            return uniprot_id.upper()
    logger.error("Connection error. Exceeded retries")
    return ""


def get_gene_id(
    uniprot_id: str, retries: int, timeout: int, logger: logging.Logger
) -> str:
    for _ in range(retries):
        try:
            response = rq.get(
                f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.txt",
                timeout=timeout,
            )
        except Exception:  # pragma: no cover
            logger.warning("Connection timeout. Retrying...")
            continue
        if response.status_code == 200:
            logger.debug("Connected to UniProt")
            content = response.text.split("\n")
            response.close()
            for line in content:
                if "GeneID;" in line:
                    gene_id = line.split(";")[1].strip()
                    logger.debug(f"Found GeneID for {uniprot_id}: {gene_id}")
                    return gene_id
            logger.error(f"GeneID for {uniprot_id} not found")
            return ""
    logger.error("Connection error. Exceeded retries")
    return ""
