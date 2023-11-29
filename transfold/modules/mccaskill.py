# Author: Filip Hajdyła
# Date of creation: 14/11/2023
# Description: Implementation of simplified McCaskill algorithm
#              for RNA secondary structure prediction

import logging

import numpy as np


def check_sequence(seq: str, logger: logging.Logger) -> bool:
    logger.info("Checking sequence")
    allowed_bases = ["A", "U", "G", "C"]
    logger.debug(f"Allowed bases: {allowed_bases}")
    for base in seq:
        logger.debug(f"Checking base: {base}")
        if base not in allowed_bases:
            logger.critical("Sequence is not valid")
            return False
    logger.info("Sequence is valid")
    return True


def check_pairing(base1: str, base2: str, logger: logging.Logger) -> bool:
    pairing_bases = [("A", "U"), ("G", "C"), ("G", "U")]
    if (base1, base2) in pairing_bases or (base2, base1) in pairing_bases:
        logger.debug(f"Checking pair {base1}-{base2}: TRUE")
        return True
    else:
        logger.debug(f"Checking pair {base1}-{base2}: FALSE")
        return False


def create_scoring_tables(
    seq: str,
    iters: int,
    bp_energy_weight: int,
    normalized_rt: int,
    min_loop_length: int,
    logger: logging.Logger,
) -> tuple[np.ndarray, np.ndarray]:
    logger.info(f"Creating scoring tables for seq: {seq}")
    logger.info(
        "PARAMS:\n"
        f"\n\titers: {iters}\n"
        f"\tbp_energy_weight: {bp_energy_weight}\n"
        f"\tnormalized_rt: {normalized_rt}\n"
        f"\tmin_loop_length: {min_loop_length}\n"
    )
    n = len(seq) + 1
    q_paired = np.zeros((n, n))
    q_unpaired = np.ones((n, n))
    for iteration in range(iters):
        logger.debug(f"Iteration: {iteration + 1}")
        for i, j in np.ndindex(q_unpaired.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            q_paired[i][j] = (
                q_unpaired[i + 1][j - 1]
                * np.exp(-bp_energy_weight / normalized_rt)
                if check_pairing(seq[i - 1], seq[j - 1], logger)
                else 0
            )
            ks = [k for k in range(i, j) if i <= k < j - min_loop_length]
            q_unpaired[i][j] = q_unpaired[i][j - 1] + sum(
                q_unpaired[i][k - 1] * q_paired[k][j] for k in ks
            )
        logger.debug(f"q_paired:\n{q_paired.shape}\t{q_paired.tolist()}\n")
        logger.debug(f"q_unpaired:\n{q_paired.shape}\t{q_unpaired.tolist()}\n")
    q_unpaired.astype(np.float64)
    q_paired.astype(np.float64)
    return q_unpaired, q_paired


def calc_paired_unpaired_probabilities(
    q: np.ndarray,
    qbp: np.ndarray,
    iters,
    bp_energy_weight: int,
    normalized_rt: int,
    logger: logging.Logger,
) -> tuple[np.ndarray, np.ndarray]:
    logger.info(
        "PARAMS:\n"
        f"\n\titers: {iters}\n"
        f"\tbp_energy_weight: {bp_energy_weight}\n"
        f"\tnormalized_rt: {normalized_rt}\n"
    )
    logger.info("Calculating paired and unpaired probabilities")
    p_paired = np.zeros(qbp.shape)
    p_unpaired = np.zeros(q.shape)
    for iteration in range(iters):
        logger.debug(f"Iteration: {iteration + 1}")
        for i, j in np.ndindex(p_unpaired.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            ks = [k for k in range(i, j) if k < i]  # noqa
            ls = [l for l in range(i, j) if j < l]  # noqa
            try:
                p_paired[i][j] = (
                    q[1][i - 1]
                    * qbp[i][j]
                    * q[j + 1][len(q) - 1]
                    / q[1][len(q) - 1]
                ) + sum(
                    p_paired[k][l]
                    * (
                        np.exp(-bp_energy_weight / normalized_rt)
                        * qbp[k + 1][l - 1]
                        * qbp[i][j]
                        * q[j + 1][l - 1]
                    )
                    / qbp[k][l]
                    for k, l in zip(ks, ls)
                )
                p_unpaired[i][j] = (
                    q[1][i - 1] * q[j + 1][len(q) - 1] / q[1][len(q) - 1]
                ) + sum(
                    p_paired[k][l]
                    * (
                        np.exp(-bp_energy_weight / normalized_rt)
                        * q[k + 1][i - 1]
                        * q[j + 1][l - 1]
                    )
                    / qbp[k][l]
                    for k, l in zip(ks, ls)
                )
            except IndexError:
                pass
        logger.debug(f"p_paired:\n{p_paired.shape}\t{p_paired.tolist()}\n")
        logger.debug(f"p_unpaired:\n{p_paired.shape}\t{p_unpaired.tolist()}\n")
    return p_unpaired[1:, 1:], p_paired[1:, 1:]
