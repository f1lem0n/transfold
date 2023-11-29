import shutil
from pathlib import Path
from time import localtime, strftime

from transfold.modules.downloaders import Writeable, cds_downloader
from transfold.modules.logger import get_logger
from transfold.modules.scope_parser import get_scope_df

SCOPE_PATH = Path("tests/data/test_scope.tsv").absolute()
PATTERN = ".*"
OUTPUT = Path("tests/data/").absolute()
RETRIES = 5
TIMEOUT = 15
LOGS_PATH = Path("tests/logs").absolute()

start_time = strftime("%Y-%m-%d_%H%M%S", localtime())
logger = get_logger(LOGS_PATH, "test_downloaders", start_time)


def test_cds_downloader():
    scope_df = get_scope_df(SCOPE_PATH, PATTERN, logger)
    (OUTPUT / "temp").mkdir(parents=True)
    (OUTPUT / "CDS" / "a.1.1.2" / "1idr" / "data").mkdir(parents=True)
    assert (
        type(cds_downloader(scope_df, OUTPUT, RETRIES, TIMEOUT, logger))
        == Writeable
    )
    cds_downloader(scope_df, OUTPUT, RETRIES, TIMEOUT, logger)
    for pdb_id in ["1ux8", "2gkm", "2gl3"]:
        assert (
            OUTPUT / "CDS" / "a.1.1.1" / pdb_id / "data" / "data_report.jsonl"
        ).exists()
        assert (
            OUTPUT
            / "CDS"
            / "a.1.1.1"
            / pdb_id
            / "data"
            / "dataset_catalog.json"
        ).exists()
    assert not (
        OUTPUT / "CDS" / "a.1.1.2" / "1idr" / "data" / "data_report.jsonl"
    ).exists()
    if (OUTPUT / "CDS").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT / "CDS")
    if (OUTPUT / "temp").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT / "temp")
