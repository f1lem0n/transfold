# Author: Filip Hajdyła
# Date of creation: 14/11/2023
# Description: Implementation of simplified McCaskill algorithm
#              for RNA secondary structure prediction

from sys import argv

import numpy as np

# global variables
MIN_LOOP_LENGTH = 1
BP_ENERGY_WEIGHT = -1
NORMALIZED_RT = 1


class stdout:
    """Methods for printing to stdout"""

    @staticmethod
    def print_params(seq: str):
        header = "{:<20} {:>20}".format("Variable", "Value")
        print("=" * len(header))
        print(header)
        print("=" * len(header))
        print("{:<20} {:>20}".format("MIN_LOOP_LENGTH", MIN_LOOP_LENGTH))
        print("{:<20} {:>20}".format("BP_ENERGY_WEIGHT", BP_ENERGY_WEIGHT))
        print("{:<20} {:>20}".format("NORMALIZED_RT", NORMALIZED_RT))
        print("-" * len(header))
        print(f"Sequence: {seq}\n")
        return stdout()


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
    seq: str, iters: int
) -> tuple[np.ndarray, np.ndarray]:
    # TODO define equation for iters if possible
    n = len(seq) + 1
    qbp = np.zeros((n, n))
    q = np.ones((n, n))
    for _ in range(iters):
        for i, j in np.ndindex(q.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            qbp[i][j] = (
                q[i + 1][j - 1] * np.exp(-BP_ENERGY_WEIGHT / NORMALIZED_RT)
                if check_pairing(seq[i - 1], seq[j - 1])
                else 0
            )
            ks = [k for k in range(i, j) if i <= k < j - MIN_LOOP_LENGTH]
            q[i][j] = q[i][j - 1] + sum(q[i][k - 1] * qbp[k][j] for k in ks)
    q.astype(np.float64)
    qbp.astype(np.float64)
    return q, qbp


def calc_paired_unpaired_probabilities(
    q: np.ndarray, qbp: np.ndarray, iters
) -> tuple[np.ndarray, np.ndarray]:
    p = np.zeros(q.shape)
    pbp = np.zeros(qbp.shape)
    for _ in range(iters):
        for i, j in np.ndindex(p.shape):
            # 1-based indexing and skipping fields below diagonal
            if j == 0 or i == 0 or i > j:
                continue
            ks = [k for k in range(i, j) if k < i]  # noqa
            ls = [l for l in range(i, j) if j < l]  # noqa
            try:
                pbp[i][j] = (
                    q[1][i - 1]
                    * qbp[i][j]
                    * q[j + 1][len(q) - 1]
                    / q[1][len(q) - 1]
                ) + sum(
                    pbp[k][l]
                    * (
                        np.exp(-BP_ENERGY_WEIGHT / NORMALIZED_RT)
                        * qbp[k + 1][l - 1]
                        * qbp[i][j]
                        * q[j + 1][l - 1]
                    )
                    / qbp[k][l]
                    for k, l in zip(ks, ls)
                )
                p[i][j] = (
                    q[1][i - 1] * q[j + 1][len(q) - 1] / q[1][len(q) - 1]
                ) + sum(
                    pbp[k][l]
                    * (
                        np.exp(-BP_ENERGY_WEIGHT / NORMALIZED_RT)
                        * q[k + 1][i - 1]
                        * q[j + 1][l - 1]
                    )
                    / qbp[k][l]
                    for k, l in zip(ks, ls)
                )
            except IndexError:
                pass
    return p[1:, 1:], pbp[1:, 1:]


def main() -> stdout:  # pragma: no cover
    seq = argv[1]
    if not check_sequence(seq):
        print("Invalid sequence!")
        exit(1)
    stdout.print_params(seq)
    q, qbp = create_scoring_tables(seq, 5)
    p, pbp = calc_paired_unpaired_probabilities(q, qbp, 5)
    print(f"P:\n{p.round(2)}\n")
    print(f"Pbp:\n{pbp.round(2)}\n")
    return stdout()


if __name__ == "__main__":
    main()  # pragma: no cover
