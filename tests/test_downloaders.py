import shutil
from pathlib import Path
from time import localtime, strftime

from transfold.modules.downloaders import Writeable, download_sequence_data
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


def test_download_sequence_data():
    scope_df = get_scope_df(SCOPE_PATH, PATTERN, logger)
    (OUTPUT / "temp").mkdir(parents=True)
    (OUTPUT / "sequence_data" / "a.1.1.2" / "1idr" / "data").mkdir(
        parents=True
    )
    assert (
        type(
            download_sequence_data(scope_df, OUTPUT, RETRIES, TIMEOUT, logger)
        )
        == Writeable
    )
    download_sequence_data(scope_df, OUTPUT, RETRIES, TIMEOUT, logger)
    for pdb_id in ["1ux8", "2gkm", "2gl3"]:
        assert (
            OUTPUT
            / "sequence_data"
            / "a.1.1.1"
            / pdb_id
            / "data"
            / "data_report.jsonl"
        ).exists()
        assert (
            OUTPUT
            / "sequence_data"
            / "a.1.1.1"
            / pdb_id
            / "data"
            / "dataset_catalog.json"
        ).exists()
    assert not (
        OUTPUT
        / "sequence_data"
        / "a.1.1.2"
        / "1idr"
        / "data"
        / "data_report.jsonl"
    ).exists()
    if (OUTPUT / "sequence_data").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT / "sequence_data")
    if (OUTPUT / "temp").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT / "temp")
