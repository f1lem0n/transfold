from pathlib import Path
import shutil

from modules.downloaders import Writeable, cds_downloader
from modules.scope_parser import get_scope_df

SCOPE_PATH = Path("tests/data/test_scope.tsv").absolute()
OUTPUT = Path("tests/data/").absolute()
RETRIES = 5
TIMEOUT = 15


def test_cds_downloader():
    scope_df = get_scope_df(SCOPE_PATH)
    (OUTPUT / "temp").mkdir(parents=True)
    (OUTPUT / "CDS" / "a.1.1.2" / "1idr" / "data").mkdir(parents=True)
    assert (
        type(
            cds_downloader(scope_df, OUTPUT, retries=RETRIES, timeout=TIMEOUT)
        )
        == Writeable
    )
    for pdb_id in ["1ux8", "2gkm", "2gl3"]:
        assert (
            OUTPUT / "CDS" / "a.1.1.1" / pdb_id / "data" / "gene.fna"
        ).exists()
    assert not (
        OUTPUT / "CDS" / "a.1.1.2" / "1idr" / "data" / "gene.fna"
    ).exists()
    shutil.rmtree(OUTPUT / "CDS")
