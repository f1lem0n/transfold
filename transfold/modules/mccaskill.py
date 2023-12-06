import logging
from os import walk
from pathlib import Path
from typing import Generator

import numpy as np


class McCaskill(object):
    """
    Calculate and serialize base pairing probabilities
    for given RNA sequences using the McCaskill algorithm.
    """

    def __init__(
        self,
        sequence_data_path: Path,
        output_path: Path,
        bp_energy_weight: int,
        normalized_rt: int,
        min_loop_length: int,
        iters: int,
        logger: logging.Logger,
        verbose=False,
    ):
        self.sequence_data_path = sequence_data_path
        self.output_path = output_path
        self.iters = iters
        self.bp_energy_weight = bp_energy_weight
        self.normalized_rt = normalized_rt
        self.min_loop_length = min_loop_length
        self.logger = logger
        self.verbose = verbose

    def _get_sequence_filepaths(self) -> Generator:
        self.logger.info(f"Reading sequence data: {self.sequence_data_path}")
        for prefix, _, files in walk(self.sequence_data_path):
            for file in files:
                if file.endswith(".fna"):
                    yield Path(prefix) / file

    def _check_sequence(self, seq: str) -> bool:
        self.logger.info("Checking sequence")
        allowed_bases = ["A", "U", "G", "C"]
        self.logger.debug(f"Allowed bases: {allowed_bases}")
        for base in seq:
            self.logger.debug(f"Checking base: {base}")
            if base not in allowed_bases:
                self.logger.critical("Sequence is not valid")
                return False
        self.logger.info("Sequence is valid")
        return True

    def _check_pairing(self, base1: str, base2: str) -> bool:
        pairing_bases = [("A", "U"), ("G", "C"), ("G", "U")]
        if (base1, base2) in pairing_bases or (base2, base1) in pairing_bases:
            self.logger.debug(f"Checking pair {base1}-{base2}: TRUE")
            return True
        else:
            self.logger.debug(f"Checking pair {base1}-{base2}: FALSE")
            return False

    # for now cannot be sped up with numba
    # because it's a recursive formula
    def _calc_scores(
        self, q_unpaired: np.ndarray, q_paired: np.ndarray, seq: str
    ) -> tuple[np.ndarray, np.ndarray]:
        for i, j in np.ndindex(q_unpaired.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            ks = [k for k in range(i, j) if i <= k < j - self.min_loop_length]
            q_unpaired[i][j] = q_unpaired[i][j - 1] + np.sum(
                [q_unpaired[i][k - 1] * q_paired[k][j] for k in ks]
            )
            q_paired[i][j] = (
                q_unpaired[i + 1][j - 1]
                * np.exp(-self.bp_energy_weight / self.normalized_rt)
                if self._check_pairing(seq[i - 1], seq[j - 1])
                else 0
            )
        return q_unpaired, q_paired

    def _create_scoring_tables(
        self,
        seq: str,
    ) -> tuple[np.ndarray, np.ndarray]:
        self.logger.info(f"Creating scoring tables for seq: {seq}")
        self.logger.info(
            "PARAMS:\n"
            f"\n\tIterations: {self.iters}\n"
            f"\tBP energy weight: {self.bp_energy_weight}\n"
            f"\tNormalized RT: {self.normalized_rt}\n"
            f"\tMinimal loop length: {self.min_loop_length}\n"
        )
        n = len(seq) + 1
        q_unpaired = np.ones((n, n))
        q_paired = np.zeros((n, n))
        for iteration in range(self.iters):
            self.logger.debug(f"Iteration: {iteration + 1}")
            q_unpaired, q_paired = self._calc_scores(q_unpaired, q_paired, seq)
            self.logger.debug(
                f"q_unpaired:\n{q_paired.shape}"
                f"\t{q_unpaired.round(2).tolist()}"
            )
            self.logger.debug(
                f"q_paired:\n{q_paired.shape}"
                f"\t{q_paired.round(2).tolist()}\n"
            )
        q_unpaired.astype(np.float64)
        q_paired.astype(np.float64)
        return q_unpaired, q_paired

    # for now cannot be sped up with numba
    # because it's a recursive formula
    def _calc_probabilities(
        self,
        p_unpaired: np.ndarray,
        p_paired: np.ndarray,
        q_unpaired: np.ndarray,
        q_paired: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        for i, j in np.ndindex(p_unpaired.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            ks = [k for k in range(i, j) if k < i]  # noqa
            ls = [l for l in range(i, j) if j < l]  # noqa
            try:
                p_paired[i][j] = (
                    q_unpaired[1][i - 1]
                    * q_paired[i][j]
                    * q_unpaired[j + 1][len(q_unpaired) - 1]
                    / q_unpaired[1][len(q_unpaired) - 1]
                ) + np.sum(
                    [
                        p_paired[k][l]
                        * (
                            np.exp(-self.bp_energy_weight / self.normalized_rt)
                            * q_paired[k + 1][l - 1]
                            * q_paired[i][j]
                            * q_unpaired[j + 1][l - 1]
                        )
                        / q_paired[k][l]
                        for k, l in zip(ks, ls)
                    ]
                )
                p_unpaired[i][j] = (
                    q_unpaired[1][i - 1]
                    * q_unpaired[j + 1][len(q_unpaired) - 1]
                    / q_unpaired[1][len(q_unpaired) - 1]
                ) + np.sum(
                    [
                        p_paired[k][l]
                        * (
                            np.exp(-self.bp_energy_weight / self.normalized_rt)
                            * q_unpaired[k + 1][i - 1]
                            * q_unpaired[j + 1][l - 1]
                        )
                        / q_paired[k][l]
                        for k, l in zip(ks, ls)
                    ]
                )
            except IndexError:
                pass
        return p_unpaired, p_paired

    def _create_probability_tables(
        self,
        q_unpaired: np.ndarray,
        q_paired: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        self.logger.info(
            "PARAMS:\n"
            f"\n\tIterations: {self.iters}\n"
            f"\tBP energy weight: {self.bp_energy_weight}\n"
            f"\tNormalized RT: {self.normalized_rt}\n"
        )
        self.logger.info("Calculating paired and unpaired probabilities")
        p_unpaired = np.zeros(q_unpaired.shape)
        p_paired = np.zeros(q_paired.shape)
        for iteration in range(self.iters):
            self.logger.debug(f"Iteration: {iteration + 1}")
            p_unpaired, p_paired = self._calc_probabilities(
                p_unpaired, p_paired, q_unpaired, q_paired
            )
            self.logger.debug(
                f"p_unpaired:\n{p_paired.shape}"
                f"\t{p_unpaired.round(2).tolist()}"
            )
            self.logger.debug(
                f"p_paired:\n{p_paired.shape}"
                f"\t{p_paired.round(2).tolist()}\n"
            )
        return p_unpaired[1:, 1:], p_paired[1:, 1:]
