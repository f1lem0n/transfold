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


def get_categories(scope_df: pd.DataFrame) -> list[str]:
    known_categories = (
        scope_df["category"].str.split(".", expand=True)[0].unique()
    ).tolist()
    return known_categories


def get_pdb_ids(scope_df: pd.DataFrame) -> list[str]:
    return scope_df["pdb_id"].unique().tolist()


def get_uniprot_id(pdb_id: str, retries=3) -> str:
    for _ in range(retries):
        response = rq.get(
            f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/1"
        )
        if response.status_code == 200:
            content = response.json()
            uniprot_id = content["rcsb_polymer_entity_container_identifiers"][
                "uniprot_ids"
            ][0]
            return uniprot_id.upper()
    return ""


def get_gene_id(uniprot_id: str, retries=3) -> str:
    for _ in range(retries):
        response = rq.get(
            f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.txt",
            timeout=10,
        )
        if response.status_code == 200:
            content = response.text.split("\n")
            for line in content:
                if "GeneID;" in line:
                    return line.split(";")[1].strip()
    return ""


for uniprot_id in [
    "O31607",
    "P15160",
    "P15160",
    "Q08753",
    "Q08753",
    "P9WN25",
    "P9WN25",
    "P9WN25",
    "P9WN25",
    "P9WN25",
]:
    print(get_gene_id(uniprot_id))
