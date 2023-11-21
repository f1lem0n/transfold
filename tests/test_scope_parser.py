from pathlib import Path

from modules.scope_parser import (
    get_category,
    get_gene_id,
    get_pdb_ids,
    get_scope_df,
    get_uniprot_id,
)

# do not change this params
SCOPE_PATH = Path("tests/data/test_scope.tsv").absolute()
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
RETRIES = 5
TIMEOUT = 15


def test_get_category():
    assert type(get_category(get_scope_df(SCOPE_PATH), TRUE_PDB_ID)) == str
    assert type(get_category(get_scope_df(SCOPE_PATH), FALSE_PDB_ID)) == str
    assert get_category(get_scope_df(SCOPE_PATH), TRUE_PDB_ID) == "a.1.1.1"
    assert get_category(get_scope_df(SCOPE_PATH), FALSE_PDB_ID) == ""


def test_get_pdb_ids():
    get_pdb_ids(get_scope_df(SCOPE_PATH)) == PDB_IDS_FROM_SCOPES


def test_get_uniprot_id():
    assert type(get_uniprot_id(TRUE_PDB_ID, RETRIES, TIMEOUT)) == str
    assert type(get_uniprot_id(FALSE_PDB_ID, RETRIES, TIMEOUT)) == str
    for pdb_id, uniprot_id in zip(
        PDB_IDS_FROM_SCOPES, UNIPROT_IDS_FROM_SCOPES
    ):
        assert get_uniprot_id(pdb_id, RETRIES, TIMEOUT) == uniprot_id
    assert get_uniprot_id(FALSE_PDB_ID, RETRIES, TIMEOUT) == ""


def test_get_gene_id():
    assert type(get_gene_id(TRUE_UNIPROT_ID, RETRIES, TIMEOUT)) == str
    assert type(get_gene_id(FALSE_UNIPROT_ID, RETRIES, TIMEOUT)) == str
    for uniprot_id, gene_id in zip(
        UNIPROT_IDS_FROM_SCOPES, GENE_IDS_FROM_SCOPES
    ):
        assert get_gene_id(uniprot_id, RETRIES, TIMEOUT) == gene_id
    assert get_gene_id(FALSE_UNIPROT_ID, RETRIES, TIMEOUT) == ""
