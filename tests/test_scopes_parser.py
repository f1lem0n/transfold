from pathlib import Path

from modules.scopes_parser import (
    get_categories,
    get_pdb_ids,
    get_protein_sequence,
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


def test_get_protein_sequence():
    assert get_protein_sequence("1ux8") == (
        "MGQSFNAPYEAIGEELLSQLVDTFYERVASHPLLKPIFPSDLTE"
        "TARKQKQFLTQYLGGPPLYTEEHGHPMLRARHLPFPITNERADA"
        "WLSCMKDAMDHVGLEGEIREFLFGRLELTARHMVNQTEAEDRSS"
    )
    assert get_protein_sequence("false_pdb_id") == ""
