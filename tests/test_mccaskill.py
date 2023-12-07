import json
import shutil
from os import walk
from pathlib import Path
from time import localtime, strftime
from typing import Generator

import numpy as np

from transfold.modules.logger import TransfoldLogger
from transfold.modules.mccaskill import McCaskill

# do not change these params
SEQ_DATA_PATH = Path("tests/data/test_sequence_data/").absolute()
OUTPUT_PATH = Path("tests/data/").absolute()
LOGS_PATH = Path("tests/logs").absolute()
MIN_LOOP_LENGTH = 1
BP_ENERGY_WEIGHT = -1
NORMALIZED_RT = 1
ITERS = 5
JOBS = 16
VALID_SEQ = "GGUCCAC"
INVALID_SEQ = "GGTCCACZ"

start_time = strftime("%Y-%m-%d_%H%M%S", localtime())
logger = TransfoldLogger(LOGS_PATH, "test_mccaskill", start_time)


def test_McCaskill():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    calculator.start()
    generated = []
    for prefix, _, suffixes in walk(
        OUTPUT_PATH / "structure_data"
    ):  # pragma: no cover
        for suffix in suffixes:
            generated.append(Path(prefix) / suffix)
    reference = []
    for prefix, _, suffixes in walk(
        OUTPUT_PATH / "test_structure_data"
    ):  # pragma: no cover
        for suffix in suffixes:
            reference.append(Path(prefix) / suffix)
    for gen, ref in zip(
        sorted(generated), sorted(reference)
    ):  # pragma: no cover
        with open(gen, "rb") as gen_file, open(ref, "rb") as ref_file:
            gen_data = json.load(gen_file)
            ref_data = json.load(ref_file)
            assert gen_data == ref_data
    # not deleting the generated files here because
    # they are used in test_McCaskill_verbose()
    # to also test if they are skipped correctly


def test_McCaskill_verbose():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=True,
    )
    calculator.start()
    generated = []
    for prefix, _, suffixes in walk(
        OUTPUT_PATH / "structure_data"
    ):  # pragma: no cover
        for suffix in suffixes:
            generated.append(Path(prefix) / suffix)
    reference = []
    for prefix, _, suffixes in walk(
        OUTPUT_PATH / "test_structure_data"
    ):  # pragma: no cover
        for suffix in suffixes:
            reference.append(Path(prefix) / suffix)
    for gen, ref in zip(
        sorted(generated), sorted(reference)
    ):  # pragma: no cover
        with open(gen, "rb") as gen_file, open(ref, "rb") as ref_file:
            gen_data = json.load(gen_file)
            ref_data = json.load(ref_file)
            assert gen_data == ref_data
    if Path(OUTPUT_PATH / "structure_data").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH / "structure_data")


def test_get_sequence_filepaths():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert isinstance(calculator._get_sequence_filepaths(), Generator)
    assert len(list(calculator._get_sequence_filepaths())) == 5
    assert str(sorted(list(calculator._get_sequence_filepaths()))[0]) == str(
        SEQ_DATA_PATH / "a.1.1.1" / "1ux8" / "data" / "gene.fna"
    )
    assert str(sorted(list(calculator._get_sequence_filepaths()))[1]) == str(
        SEQ_DATA_PATH / "a.1.1.1" / "2gkm" / "data" / "gene.fna"
    )
    assert str(sorted(list(calculator._get_sequence_filepaths()))[2]) == str(
        SEQ_DATA_PATH / "a.1.1.1" / "2gl3" / "data" / "gene.fna"
    )
    assert str(sorted(list(calculator._get_sequence_filepaths()))[3]) == str(
        SEQ_DATA_PATH / "a.1.1.2" / "1idr" / "data" / "cds.fna"
    )
    assert str(sorted(list(calculator._get_sequence_filepaths()))[4]) == str(
        SEQ_DATA_PATH / "a.1.1.2" / "1idr" / "data" / "gene.fna"
    )


def test_get_sequences():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert isinstance(calculator._get_sequences_and_metadata(), Generator)
    assert len(list(calculator._get_sequences_and_metadata())) == 7


def test_get_structure():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    seq, description, category, pdb_id, source, idx = list(
        calculator._get_sequences_and_metadata()
    )[1]
    calculator._get_structure(seq, description, category, pdb_id, source, idx)
    # second time should be skipped
    calculator._get_structure(seq, description, category, pdb_id, source, idx)
    with open(
        OUTPUT_PATH
        / "test_structure_data"
        / "a.1.1.1"
        / "1ux8"
        / "gene"
        / "structure_1.json",
        "rb",
    ) as ref_file, open(
        OUTPUT_PATH
        / "structure_data"
        / "a.1.1.1"
        / "1ux8"
        / "gene"
        / "structure_1.json",
        "rb",
    ) as gen_file:
        gen_data = json.load(gen_file)
        ref_data = json.load(ref_file)
        assert gen_data == ref_data
    seq, description, category, pdb_id, source, idx = list(
        calculator._get_sequences_and_metadata()
    )[3]
    calculator._get_structure(seq, description, category, pdb_id, source, idx)
    assert not Path(
        OUTPUT_PATH
        / "structure_data"
        / "a.1.1.1"
        / "2gkm"
        / "gene"
        / "structure_1.json"
    ).exists()
    if Path(OUTPUT_PATH / "structure_data").exists():  # pragma: no cover
        shutil.rmtree(OUTPUT_PATH / "structure_data")


def test_check_sequence():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert calculator._check_sequence(VALID_SEQ)
    assert not calculator._check_sequence(INVALID_SEQ)


def test_check_pairing():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert type(calculator._check_pairing("A", "U")) == bool
    assert calculator._check_pairing("A", "U") is True
    assert calculator._check_pairing("U", "U") is False
    assert calculator._check_pairing("G", "U") is True
    assert calculator._check_pairing("C", "U") is False
    assert calculator._check_pairing("A", "C") is False
    assert calculator._check_pairing("G", "C") is True
    assert calculator._check_pairing("C", "C") is False
    assert calculator._check_pairing("A", "G") is False
    assert calculator._check_pairing("A", "A") is False


def test_calc_scores():
    # testing only shapes of intermediate arrays because target values
    # are already tested in test_create_scoring_tables()
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    n = len(VALID_SEQ) + 1
    q_unpaired = np.ones((n, n))
    q_paired = np.zeros((n, n))
    assert calculator._calc_scores(q_unpaired, q_paired, VALID_SEQ)[
        0
    ].shape == (n, n)
    assert calculator._calc_scores(q_unpaired, q_paired, VALID_SEQ)[
        1
    ].shape == (n, n)


def test_create_scoring_tables():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert (
        type(
            calculator._create_scoring_tables(
                VALID_SEQ,
            )
        )
        == tuple
    )
    assert (
        type(
            calculator._create_scoring_tables(
                VALID_SEQ,
            )[0]
        )
        == np.ndarray
    )
    assert (
        type(
            calculator._create_scoring_tables(
                VALID_SEQ,
            )[1]
        )
        == np.ndarray
    )
    assert calculator._create_scoring_tables(
        VALID_SEQ,
    )[
        0
    ].shape == (8, 8)
    assert calculator._create_scoring_tables(
        VALID_SEQ,
    )[
        1
    ].shape == (8, 8)
    np.testing.assert_array_equal(
        calculator._create_scoring_tables(
            VALID_SEQ,
        )[
            1
        ].round(2),
        np.array(
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
        ),
        verbose=True,
    )
    np.testing.assert_array_equal(
        calculator._create_scoring_tables(
            VALID_SEQ,
        )[
            0
        ].round(2),
        np.array(
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
        ),
    )


def test_calc_probabilities():
    # testing only shapes of intermediate arrays because target values
    # are already tested in test_create_probability_tables()
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    n = len(VALID_SEQ) + 1
    q_unpaired = np.ones((n, n))
    q_paired = np.zeros((n, n))
    p_unpaired = np.zeros(q_unpaired.shape)
    p_paired = np.zeros(q_paired.shape)
    assert calculator._calc_probabilities(
        p_unpaired, p_paired, q_unpaired, q_paired
    )[0].shape == (n, n)
    assert calculator._calc_probabilities(
        p_unpaired, p_paired, q_unpaired, q_paired
    )[1].shape == (n, n)


def test_create_probability_tables():
    calculator = McCaskill(
        sequence_data_path=SEQ_DATA_PATH,
        output=OUTPUT_PATH,
        bp_energy_weight=BP_ENERGY_WEIGHT,
        normalized_rt=NORMALIZED_RT,
        min_loop_length=MIN_LOOP_LENGTH,
        iters=ITERS,
        jobs=JOBS,
        logger=logger,
        verbose=False,
    )
    assert (
        type(
            calculator._create_probability_tables(
                *calculator._create_scoring_tables(
                    VALID_SEQ,
                ),
            )
        )
        == tuple
    )
    assert (
        type(
            calculator._create_probability_tables(
                *calculator._create_scoring_tables(
                    VALID_SEQ,
                ),
            )[0]
        )
        == np.ndarray
    )
    assert (
        type(
            calculator._create_probability_tables(
                *calculator._create_scoring_tables(
                    VALID_SEQ,
                ),
            )[1]
        )
        == np.ndarray
    )
    assert calculator._create_probability_tables(
        *calculator._create_scoring_tables(
            VALID_SEQ,
        ),
    )[0].shape == (7, 7)
    assert calculator._create_probability_tables(
        *calculator._create_scoring_tables(
            VALID_SEQ,
        ),
    )[1].shape == (7, 7)
    np.testing.assert_array_equal(
        calculator._create_probability_tables(
            *calculator._create_scoring_tables(
                VALID_SEQ,
            ),
        )[0].round(2),
        np.array(
            [
                [0.32, 0.06, 0.02, 0.02, 0.02, 0.02, 0.0],
                [0.0, 0.06, 0.02, 0.02, 0.02, 0.02, 0.0],
                [0.0, 0.0, 0.02, 0.02, 0.02, 0.02, 0.0],
                [0.0, 0.0, 0.0, 0.06, 0.06, 0.06, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.15, 0.15, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.37, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        ),
    )
    np.testing.assert_array_equal(
        calculator._create_probability_tables(
            *calculator._create_scoring_tables(
                VALID_SEQ,
            ),
        )[1].round(2),
        np.array(
            [
                [0.0, 0.0, 0.05, 0.05, 0.17, 0.0, 0.0],
                [0.0, 0.0, 0.05, 0.05, 0.05, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        ),
    )
