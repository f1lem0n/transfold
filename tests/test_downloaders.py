import shutil
from pathlib import Path
from time import localtime, strftime

from transfold.modules.downloaders import SequenceDataDownloader, Writeable
from transfold.modules.logger import TransfoldLogger

# do not change this params
SCOPE_PATH = Path("tests/data/test_scope.tsv").absolute()
OUTPUT_PATH = Path("tests/data/sequence_data/").absolute()
LOGS_PATH = Path("tests/logs").absolute()
PATTERN = ".*"
JOBS = 16
RETRIES = 5
TIMEOUT = 15
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

start_time = strftime("%Y-%m-%d_%H%M%S", localtime())
logger = TransfoldLogger(LOGS_PATH, "test_scope_parser", start_time)


def test_SequenceDataDownloader():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    (OUTPUT_PATH / "temp").mkdir(parents=True)
    (OUTPUT_PATH / "a.1.1.2" / "1idr" / "data").mkdir(parents=True)
    assert type(downloader.start()) == Writeable
    downloader.start()
    for pdb_id in ["1ux8", "2gkm", "2gl3"]:
        assert (
            OUTPUT_PATH / "a.1.1.1" / pdb_id / "data" / "data_report.jsonl"
        ).exists()
        assert (
            OUTPUT_PATH / "a.1.1.1" / pdb_id / "data" / "dataset_catalog.json"
        ).exists()
    assert not (
        OUTPUT_PATH / "a.1.1.2" / "1idr" / "data" / "data_report.jsonl"
    ).exists()
    if OUTPUT_PATH.exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH)
    if (OUTPUT_PATH / "temp").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH / "temp")


def test_SequenceDataDownloader_verbose():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=True,
    )
    (OUTPUT_PATH / "temp").mkdir(parents=True)
    (OUTPUT_PATH / "a.1.1.2" / "1idr" / "data").mkdir(parents=True)
    assert type(downloader.start()) == Writeable
    downloader.start()
    for pdb_id in ["1ux8", "2gkm", "2gl3"]:
        assert (
            OUTPUT_PATH / "a.1.1.1" / pdb_id / "data" / "data_report.jsonl"
        ).exists()
        assert (
            OUTPUT_PATH / "a.1.1.1" / pdb_id / "data" / "dataset_catalog.json"
        ).exists()
    assert not (
        OUTPUT_PATH / "a.1.1.2" / "1idr" / "data" / "data_report.jsonl"
    ).exists()
    if OUTPUT_PATH.exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH)
    if (OUTPUT_PATH / "temp").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH / "temp")


def test_download_sequence_data():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    (OUTPUT_PATH / "temp").mkdir(parents=True)
    assert type(downloader._download_sequence_data(TRUE_PDB_ID)) == Writeable
    downloader._download_sequence_data(TRUE_PDB_ID)
    assert (
        OUTPUT_PATH / "a.1.1.1" / "1ux8" / "data" / "data_report.jsonl"
    ).exists()
    downloader._download_sequence_data(FALSE_PDB_ID)
    assert not (
        OUTPUT_PATH / "a.1.1.1" / FALSE_PDB_ID / "data" / "data_report.jsonl"
    ).exists()
    # test case where UniProt ID is found but not GeneID
    downloader._download_sequence_data("1dly")
    assert not (
        OUTPUT_PATH / "a.1.1.1" / "1dly" / "data" / "data_report.jsonl"
    ).exists()
    if OUTPUT_PATH.exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH)
    if (OUTPUT_PATH / "temp").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH / "temp")


def test_get_category():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert type(downloader._get_category(TRUE_PDB_ID)) == str
    assert type(downloader._get_category(FALSE_PDB_ID)) == str
    assert downloader._get_category(TRUE_PDB_ID) == "a.1.1.1"
    assert downloader._get_category(FALSE_PDB_ID) == ""


def test_get_pdb_ids():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    downloader._get_pdb_ids() == PDB_IDS_FROM_SCOPES


def test_get_uniprot_id():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert type(downloader._get_uniprot_id(TRUE_PDB_ID)) == str
    assert type(downloader._get_uniprot_id(FALSE_PDB_ID)) == str
    for pdb_id, uniprot_id in zip(
        PDB_IDS_FROM_SCOPES, UNIPROT_IDS_FROM_SCOPES
    ):
        assert downloader._get_uniprot_id(pdb_id) == uniprot_id
    assert downloader._get_uniprot_id(FALSE_PDB_ID) == ""


def test_get_gene_id():
    downloader = SequenceDataDownloader(
        scope_path=SCOPE_PATH,
        pattern=PATTERN,
        output=OUTPUT_PATH,
        retries=RETRIES,
        timeout=TIMEOUT,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert type(downloader._get_gene_id(TRUE_UNIPROT_ID)) == str
    assert type(downloader._get_gene_id(FALSE_UNIPROT_ID)) == str
    for uniprot_id, gene_id in zip(
        UNIPROT_IDS_FROM_SCOPES, GENE_IDS_FROM_SCOPES
    ):
        assert downloader._get_gene_id(uniprot_id) == gene_id
    assert downloader._get_gene_id(FALSE_UNIPROT_ID) == ""
