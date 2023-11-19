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


def get_protein_sequence(pdb_id: str) -> str:
    response = rq.get(
        f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/1",
        timeout=10,
    ).json()
    try:
        sequence = response["entity_poly"]["pdbx_seq_one_letter_code_can"]
        return sequence.upper()
    except (
        Exception,
        rq.exceptions.RequestException,
        rq.exceptions.RequestsWarning,
        rq.exceptions.RequestsDependencyWarning,
        rq.exceptions.ConnectTimeout,
        rq.exceptions.ConnectionError,
    ):
        return ""
