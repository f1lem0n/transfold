from pathlib import Path
from time import localtime, strftime

from transfold.modules.logger import get_logger
from transfold.modules.scope_parser import (
    get_category,
    get_gene_id,
    get_pdb_ids,
    get_scope_df,
    get_uniprot_id,
)

# do not change this params
SCOPE_PATH = Path("tests/data/test_scope.tsv").absolute()
PATTERN = ".*"
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
LOGS_PATH = Path("tests/logs").absolute()

start_time = strftime("%Y-%m-%d_%H%M%S", localtime())
logger = get_logger(LOGS_PATH, "test_scope_parser", start_time)


def test_get_category():
    assert (
        type(
            get_category(
                get_scope_df(SCOPE_PATH, PATTERN, logger), TRUE_PDB_ID, logger
            )
        )
        == str
    )
    assert (
        type(
            get_category(
                get_scope_df(SCOPE_PATH, PATTERN, logger), FALSE_PDB_ID, logger
            )
        )
        == str
    )
    assert (
        get_category(
            get_scope_df(SCOPE_PATH, PATTERN, logger), TRUE_PDB_ID, logger
        )
        == "a.1.1.1"
    )
    assert (
        get_category(
            get_scope_df(SCOPE_PATH, PATTERN, logger), FALSE_PDB_ID, logger
        )
        == ""
    )


def test_get_pdb_ids():
    get_pdb_ids(
        get_scope_df(SCOPE_PATH, PATTERN, logger), logger
    ) == PDB_IDS_FROM_SCOPES


def test_get_uniprot_id():
    assert type(get_uniprot_id(TRUE_PDB_ID, RETRIES, TIMEOUT, logger)) == str
    assert type(get_uniprot_id(FALSE_PDB_ID, RETRIES, TIMEOUT, logger)) == str
    for pdb_id, uniprot_id in zip(
        PDB_IDS_FROM_SCOPES, UNIPROT_IDS_FROM_SCOPES
    ):
        assert get_uniprot_id(pdb_id, RETRIES, TIMEOUT, logger) == uniprot_id
    assert get_uniprot_id(FALSE_PDB_ID, RETRIES, TIMEOUT, logger) == ""


def test_get_gene_id():
    assert type(get_gene_id(TRUE_UNIPROT_ID, RETRIES, TIMEOUT, logger)) == str
    assert type(get_gene_id(FALSE_UNIPROT_ID, RETRIES, TIMEOUT, logger)) == str
    for uniprot_id, gene_id in zip(
        UNIPROT_IDS_FROM_SCOPES, GENE_IDS_FROM_SCOPES
    ):
        assert get_gene_id(uniprot_id, RETRIES, TIMEOUT, logger) == gene_id
    assert get_gene_id(FALSE_UNIPROT_ID, RETRIES, TIMEOUT, logger) == ""
