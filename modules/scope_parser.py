# Author: Filip Hajdyła
# Date of creation: 14/11/2023
# Description: Parser functions to get GeneID from PDB ID,
#              and category from SCOPe file

from pathlib import Path

import pandas as pd
import requests as rq


def get_scope_df(scope_path: Path) -> pd.DataFrame:
    # TODO correct column names
    scope_df = pd.read_table(
        scope_path,
        sep="\t",
        header=None,
        names=[
            "scope_id",
            "pdb_id",
            "chain",
            "category",
            "unknown_int",
            "unknown_params",
        ],
    )
    return scope_df


def get_pdb_ids(scope_df: pd.DataFrame) -> list[str]:
    return scope_df["pdb_id"].unique().tolist()


def get_category(scope_df: pd.DataFrame, pdb_id: str) -> str:
    try:
        return scope_df[scope_df["pdb_id"] == pdb_id]["category"].tolist()[0]
    except (KeyError, IndexError):
        return ""


def get_uniprot_id(pdb_id: str, retries: int, timeout: int) -> str:
    for _ in range(retries):
        try:
            response = rq.get(
                "https://data.rcsb.org/rest/"
                f"v1/core/polymer_entity/{pdb_id}/1",
                timeout=timeout,
            )
        except Exception:  # pragma: no cover
            continue
        if response.status_code == 200:
            content = response.json()
            response.close()
            uniprot_id = content["rcsb_polymer_entity_container_identifiers"][
                "uniprot_ids"
            ][0]
            return uniprot_id.upper()
    return ""


def get_gene_id(uniprot_id: str, retries: int, timeout: int) -> str:
    for _ in range(retries):
        try:
            response = rq.get(
                f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.txt",
                timeout=timeout,
            )
        except Exception:  # pragma: no cover
            continue
        if response.status_code == 200:
            content = response.text.split("\n")
            response.close()
            for line in content:
                if "GeneID;" in line:
                    return line.split(";")[1].strip()
    return ""
