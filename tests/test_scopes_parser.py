from pathlib import Path

from modules.scopes_parser import (
    get_categories,
    get_gene_id,
    get_pdb_ids,
    get_scope_df,
    get_uniprot_id,
)

# do not change this params
SCOPES_PATH = Path("tests/data/test_scopes.tsv").absolute()
TRUE_PDB_ID = "1ux8"
FALSE_PDB_ID = "false_pdb_id"
TRUE_UNIPROT_ID = "O31607"
FALSE_UNIPROT_ID = "false_uniprot_id"
PDB_IDS_FROM_SCOPES = [
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
UNIPROT_IDS_FROM_SCOPES = [
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
]
GENE_IDS_FROM_SCOPES = [
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
]


def test_get_categories():
    get_categories(get_scope_df(SCOPES_PATH)) == ["a"]


def test_get_pdb_ids():
    get_pdb_ids(get_scope_df(SCOPES_PATH)) == PDB_IDS_FROM_SCOPES


def test_get_uniprot_id():
    assert type(get_uniprot_id(TRUE_PDB_ID)) == str
    assert type(get_uniprot_id(FALSE_PDB_ID)) == str
    for pdb_id, uniprot_id in zip(
        PDB_IDS_FROM_SCOPES, UNIPROT_IDS_FROM_SCOPES
    ):
        assert get_uniprot_id(pdb_id) == uniprot_id
    assert get_uniprot_id(FALSE_PDB_ID) == ""


def test_get_gene_id():
    assert type(get_gene_id(TRUE_UNIPROT_ID)) == str
    assert type(get_gene_id(FALSE_UNIPROT_ID)) == str
    for uniprot_id, gene_id in zip(
        UNIPROT_IDS_FROM_SCOPES, GENE_IDS_FROM_SCOPES
    ):
        assert get_gene_id(uniprot_id) == gene_id
    assert get_gene_id(FALSE_UNIPROT_ID) == ""
