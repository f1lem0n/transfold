from pathlib import Path

import numpy as np

from transfold.modules.mccaskill import (
    calc_paired_unpaired_probabilities,
    check_pairing,
    check_sequence,
    create_scoring_tables,
)

# do not change these params
MIN_LOOP_LENGTH = 1
BP_ENERGY_WEIGHT = -1
NORMALIZED_RT = 1
VALID_SEQ = "GGUCCAC"
INVALID_SEQ = "GGTCCACZ"
LOGS_PATH = Path("tests/logs").absolute()


def test_check_sequence():
    assert check_sequence(VALID_SEQ, LOGS_PATH) is True
    assert check_sequence(INVALID_SEQ, LOGS_PATH) is False


def test_check_pairing():
    assert type(check_pairing("A", "U", LOGS_PATH)) == bool
    assert check_pairing("A", "U", LOGS_PATH) is True
    assert check_pairing("U", "U", LOGS_PATH) is False
    assert check_pairing("G", "U", LOGS_PATH) is True
    assert check_pairing("C", "U", LOGS_PATH) is False
    assert check_pairing("A", "C", LOGS_PATH) is False
    assert check_pairing("G", "C", LOGS_PATH) is True
    assert check_pairing("C", "C", LOGS_PATH) is False
    assert check_pairing("A", "G", LOGS_PATH) is False
    assert check_pairing("A", "A", LOGS_PATH) is False


def test_create_scoring_tables():
    assert (
        type(
            create_scoring_tables(
                VALID_SEQ,
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                MIN_LOOP_LENGTH,
                LOGS_PATH,
            )
        )
        == tuple
    )
    assert (
        type(
            create_scoring_tables(
                VALID_SEQ,
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                MIN_LOOP_LENGTH,
                LOGS_PATH,
            )[0]
        )
        == np.ndarray
    )
    assert (
        type(
            create_scoring_tables(
                VALID_SEQ,
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                MIN_LOOP_LENGTH,
                LOGS_PATH,
            )[1]
        )
        == np.ndarray
    )
    assert create_scoring_tables(
        VALID_SEQ,
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        MIN_LOOP_LENGTH,
        LOGS_PATH,
    )[0].shape == (8, 8)
    assert create_scoring_tables(
        VALID_SEQ,
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        MIN_LOOP_LENGTH,
        LOGS_PATH,
    )[1].shape == (8, 8)
    # TODO correct these tables
    create_scoring_tables(
        VALID_SEQ,
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        MIN_LOOP_LENGTH,
        LOGS_PATH,
    )[0].round(2) == np.array(
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
    create_scoring_tables(
        VALID_SEQ,
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        MIN_LOOP_LENGTH,
        LOGS_PATH,
    )[1].round(2) == np.array(
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


def test_calc_paired_unpaired_probabilities():
    assert (
        type(
            calc_paired_unpaired_probabilities(
                *create_scoring_tables(
                    VALID_SEQ,
                    3,
                    BP_ENERGY_WEIGHT,
                    NORMALIZED_RT,
                    MIN_LOOP_LENGTH,
                    LOGS_PATH,
                ),
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                LOGS_PATH,
            )
        )
        == tuple
    )
    assert (
        type(
            calc_paired_unpaired_probabilities(
                *create_scoring_tables(
                    VALID_SEQ,
                    3,
                    BP_ENERGY_WEIGHT,
                    NORMALIZED_RT,
                    MIN_LOOP_LENGTH,
                    LOGS_PATH,
                ),
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                LOGS_PATH,
            )[0]
        )
        == np.ndarray
    )
    assert (
        type(
            calc_paired_unpaired_probabilities(
                *create_scoring_tables(
                    VALID_SEQ,
                    3,
                    BP_ENERGY_WEIGHT,
                    NORMALIZED_RT,
                    MIN_LOOP_LENGTH,
                    LOGS_PATH,
                ),
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                LOGS_PATH,
            )[1]
        )
        == np.ndarray
    )
    assert calc_paired_unpaired_probabilities(
        *create_scoring_tables(
            VALID_SEQ,
            3,
            BP_ENERGY_WEIGHT,
            NORMALIZED_RT,
            MIN_LOOP_LENGTH,
            LOGS_PATH,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        LOGS_PATH,
    )[0].shape == (7, 7)
    assert calc_paired_unpaired_probabilities(
        *create_scoring_tables(
            VALID_SEQ,
            3,
            BP_ENERGY_WEIGHT,
            NORMALIZED_RT,
            MIN_LOOP_LENGTH,
            LOGS_PATH,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        LOGS_PATH,
    )[1].shape == (7, 7)
    # TODO correct these tables
    calc_paired_unpaired_probabilities(
        *create_scoring_tables(
            VALID_SEQ,
            3,
            BP_ENERGY_WEIGHT,
            NORMALIZED_RT,
            MIN_LOOP_LENGTH,
            LOGS_PATH,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        LOGS_PATH,
    )[0] == np.array(
        [
            [0.32, 0.06, 0.02, 0.02, 0.02, 0.02, 0.0],
            [0.0, 0.06, 0.02, 0.02, 0.02, 0.02, 0.0],
            [0.0, 0.0, 0.02, 0.02, 0.02, 0.02, 0.0],
            [0.0, 0.0, 0.0, 0.06, 0.06, 0.06, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.15, 0.15, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.37, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
    )
    calc_paired_unpaired_probabilities(
        *create_scoring_tables(
            VALID_SEQ,
            3,
            BP_ENERGY_WEIGHT,
            NORMALIZED_RT,
            MIN_LOOP_LENGTH,
            LOGS_PATH,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        LOGS_PATH,
    )[1] == np.array(
        [
            [0.0, 0.0, 0.05, 0.05, 0.17, 0.0, 0.0],
            [0.0, 0.0, 0.05, 0.05, 0.05, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
    )
