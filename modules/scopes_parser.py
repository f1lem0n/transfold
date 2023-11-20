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


def get_uniprot_id(pdb_id: str) -> str:
    try:
        response = rq.get(
            "https://data.rcsb.org/rest" f"/v1/core/polymer_entity/{pdb_id}/1",
            timeout=10,
        ).json()
        uniprot_id = response["rcsb_polymer_entity_container_identifiers"][
            "uniprot_ids"
        ][0]
        return uniprot_id.upper()
    except (
        Exception,
        rq.exceptions.RequestException,
        rq.exceptions.RequestsWarning,
        rq.exceptions.RequestsDependencyWarning,
        rq.exceptions.ConnectTimeout,
        rq.exceptions.ConnectionError,
    ):
        return ""


print(get_uniprot_id("1ux8"))
