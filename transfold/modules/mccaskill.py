# Author: Filip Hajdyła
# Date of creation: 14/11/2023
# Description: Implementation of simplified McCaskill algorithm
#              for RNA secondary structure prediction

import numpy as np


def check_sequence(seq: str) -> bool:
    allowed_bases = ["A", "U", "G", "C"]
    for base in seq:
        if base not in allowed_bases:
            return False
    return True


def check_pairing(base1: str, base2: str) -> bool:
    pairing_bases = [("A", "U"), ("G", "C"), ("G", "U")]
    if (base1, base2) in pairing_bases or (base2, base1) in pairing_bases:
        return True
    else:
        return False


def create_scoring_tables(
    seq: str,
    iters: int,
    bp_energy_weight: int,
    normalized_rt: int,
    min_loop_length: int,
) -> tuple[np.ndarray, np.ndarray]:
    # TODO define equation for iters if possible
    n = len(seq) + 1
    q_paired = np.zeros((n, n))
    q_unpaired = np.ones((n, n))
    for _ in range(iters):
        for i, j in np.ndindex(q_unpaired.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            q_paired[i][j] = (
                q_unpaired[i + 1][j - 1]
                * np.exp(-bp_energy_weight / normalized_rt)
                if check_pairing(seq[i - 1], seq[j - 1])
                else 0
            )
            ks = [k for k in range(i, j) if i <= k < j - min_loop_length]
            q_unpaired[i][j] = q_unpaired[i][j - 1] + sum(
                q_unpaired[i][k - 1] * q_paired[k][j] for k in ks
            )
    q_unpaired.astype(np.float64)
    q_paired.astype(np.float64)
    return q_unpaired, q_paired


def calc_paired_unpaired_probabilities(
    q: np.ndarray,
    qbp: np.ndarray,
    iters,
    bp_energy_weight: int,
    normalized_rt: int,
) -> tuple[np.ndarray, np.ndarray]:
    p_paired = np.zeros(qbp.shape)
    p_unpaired = np.zeros(q.shape)
    for _ in range(iters):
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
    return p_unpaired[1:, 1:], p_paired[1:, 1:]
