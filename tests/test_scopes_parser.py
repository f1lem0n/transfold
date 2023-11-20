from pathlib import Path

from modules.scopes_parser import (
    get_categories,
    get_gene_id,
    get_pdb_ids,
    get_scope_df,
    get_uniprot_id,
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
    assert type(get_uniprot_id("false_pdb_id")) == str
    for pdb_id, uniprot_id in zip(
        [
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
        ],
        [
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
        ],
    ):
        assert get_uniprot_id(pdb_id) == uniprot_id
    assert get_uniprot_id("false_pdb_id") == ""


def test_get_gene_id():
    assert type(get_gene_id("O31607")) == str
    assert type(get_gene_id("false_uniprot_id")) == str
    for uniprot_id, gene_id in zip(
        [
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
        ],
        [
            "936416",
            "",
            "",
            "",
            "",
            "45425525",
            "45425525",
            "45425525",
            "45425525",
            "45425525",
        ],
    ):
        assert get_gene_id(uniprot_id) == gene_id
    assert get_gene_id("false_uniprot_id") == ""
