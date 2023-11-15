import numpy as np
from pytest import CaptureFixture

from scripts.mccaskill import (
    check_pairing,
    check_sequence,
    create_scoring_tables,
    stdout,
)

# do not change these params
MIN_LOOP_LENGTH = 1
BP_ENERGY_WEIGHT = -1
NORMALIZED_RT = 1
VALID_SEQ = "GGUCCAC"
INVALID_SEQ = "GGTCCACZ"


# capsys is used to capture stdout and stderr from stdout.print_params()
def test_print_params(capsys: CaptureFixture[str]):
    assert type(stdout.print_params(VALID_SEQ)) == stdout
    captured = capsys.readouterr()
    assert (
        captured.out
        == """=========================================
Variable                            Value
=========================================
MIN_LOOP_LENGTH                         1
BP_ENERGY_WEIGHT                       -1
NORMALIZED_RT                           1
-----------------------------------------
Sequence: GGUCCAC

"""
    )


def test_check_sequence():
    assert check_sequence(VALID_SEQ) is True
    assert check_sequence(INVALID_SEQ) is False


def test_check_pairing():
    assert type(check_pairing("A", "U")) == bool
    assert check_pairing("A", "U") is True
    assert check_pairing("U", "U") is False
    assert check_pairing("G", "U") is True
    assert check_pairing("C", "U") is False
    assert check_pairing("A", "C") is False
    assert check_pairing("G", "C") is True
    assert check_pairing("C", "C") is False
    assert check_pairing("A", "G") is False
    assert check_pairing("A", "A") is False


def test_create_scorting_tables():
    assert type(create_scoring_tables(VALID_SEQ, 3)) == tuple
    assert type(create_scoring_tables(VALID_SEQ, 3)[0]) == np.ndarray
    assert type(create_scoring_tables(VALID_SEQ, 3)[1]) == np.ndarray
    assert create_scoring_tables(VALID_SEQ, 3)[0].shape == (8, 8)
    assert create_scoring_tables(VALID_SEQ, 3)[1].shape == (8, 8)
    create_scoring_tables(VALID_SEQ, 3)[0].round(2) == np.array(
        [
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 3.72, 9.15, 21.98, 24.7, 59.69],
            [1.0, 1.0, 1.0, 1.0, 3.72, 6.44, 9.15, 19.26],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.72, 3.72],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        ]
    )
    create_scoring_tables(VALID_SEQ, 3)[1].round(2) == np.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 2.72, 2.72, 10.11, 0.0, 24.89],
            [0.0, 0.0, 0.0, 2.72, 2.72, 2.72, 0.0, 10.11],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.72, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
    )
