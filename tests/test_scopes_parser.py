from pathlib import Path

from modules.scopes_parser import (
    get_categories,
    get_pdb_ids,
    get_uniprot_id,
    get_scope_df,
)

SCOPES_PATH = Path("tests/data/test_scopes.tsv").absolute()


def test_get_categories():
    get_categories(get_scope_df(SCOPES_PATH)) == ["a"]


def test_get_pdb_ids():
    get_pdb_ids(get_scope_df(SCOPES_PATH)) == [
        "1ux8",
        "1dlw",
        "1uvy",
        "1dly",
        "1uvx",
        "2gkm",
        "2gkm",
        "2gl3",
        "2gl3",
        "1idr",
    ]


def test_get_uniprot_id():
    assert type(get_uniprot_id("1ux8")) == str
    assert get_uniprot_id("1ux8") == "O31607"
    assert get_uniprot_id("false_pdb_id") == ""
