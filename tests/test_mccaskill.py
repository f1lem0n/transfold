from scripts.mccaskill import check_pairing, check_sequence, stdout

# do not change these params
MIN_LOOP_LENGTH = 1
BP_ENERGY_WEIGHT = -1
NORMALIZED_RT = 1
VALID_SEQ = "GGUCCAC"
INVALID_SEQ = "GGTCCACZ"


# capsys is used to capture stdout and stderr from stdout.print_params()
def test_print_params(capsys):
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
    assert check_pairing("A", "U") is True
    assert check_pairing("U", "U") is False
    assert check_pairing("G", "U") is True
    assert check_pairing("C", "U") is False
    assert check_pairing("A", "C") is False
    assert check_pairing("G", "C") is True
    assert check_pairing("C", "C") is False
    assert check_pairing("A", "G") is False
    assert check_pairing("A", "A") is False
