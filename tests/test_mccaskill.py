from pathlib import Path
from time import localtime, strftime

import numpy as np

from transfold.modules.logger import TransfoldLogger
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

start_time = strftime("%Y-%m-%d_%H%M%S", localtime())
logger = TransfoldLogger(LOGS_PATH, "test_mccaskill", start_time)


def test_check_sequence():
    assert check_sequence(VALID_SEQ, logger) is True
    assert check_sequence(INVALID_SEQ, logger) is False


def test_check_pairing():
    assert type(check_pairing("A", "U", logger)) == bool
    assert check_pairing("A", "U", logger) is True
    assert check_pairing("U", "U", logger) is False
    assert check_pairing("G", "U", logger) is True
    assert check_pairing("C", "U", logger) is False
    assert check_pairing("A", "C", logger) is False
    assert check_pairing("G", "C", logger) is True
    assert check_pairing("C", "C", logger) is False
    assert check_pairing("A", "G", logger) is False
    assert check_pairing("A", "A", logger) is False


def test_create_scoring_tables():
    assert (
        type(
            create_scoring_tables(
                VALID_SEQ,
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                MIN_LOOP_LENGTH,
                logger,
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
                logger,
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
                logger,
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
        logger,
    )[0].shape == (8, 8)
    assert create_scoring_tables(
        VALID_SEQ,
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        MIN_LOOP_LENGTH,
        logger,
    )[1].shape == (8, 8)
    # TODO correct these tables
    create_scoring_tables(
        VALID_SEQ,
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        MIN_LOOP_LENGTH,
        logger,
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
        logger,
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
                    logger,
                ),
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                logger,
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
                    logger,
                ),
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                logger,
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
                    logger,
                ),
                3,
                BP_ENERGY_WEIGHT,
                NORMALIZED_RT,
                logger,
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
            logger,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        logger,
    )[0].shape == (7, 7)
    assert calc_paired_unpaired_probabilities(
        *create_scoring_tables(
            VALID_SEQ,
            3,
            BP_ENERGY_WEIGHT,
            NORMALIZED_RT,
            MIN_LOOP_LENGTH,
            logger,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        logger,
    )[1].shape == (7, 7)
    # TODO correct these tables
    calc_paired_unpaired_probabilities(
        *create_scoring_tables(
            VALID_SEQ,
            3,
            BP_ENERGY_WEIGHT,
            NORMALIZED_RT,
            MIN_LOOP_LENGTH,
            logger,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        logger,
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
            logger,
        ),
        3,
        BP_ENERGY_WEIGHT,
        NORMALIZED_RT,
        logger,
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
