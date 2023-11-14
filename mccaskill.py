# Author: Filip Hajdyła
# Date of creation: 14/11/2023
# Description: Implementation of simplified McCaskill algorithm
#              for RNA secondary structure prediction
# Version: 0.1

import numpy as np
from sys import argv

# global variables

MIN_LOOP_LENGTH = 1
BP_ENERGY_WEIGHT = -1
NORMALIZED_RT = 1


class stdout:
    def print_params(seq: str):
        ...


def print_params(seq: str) -> stdout:
    header = "{:<20} {:>20}".format("Variable", "Value")
    print("=" * len(header))
    print(header)
    print("=" * len(header))
    print("{:<20} {:>20}".format("MIN_LOOP_LENGTH", MIN_LOOP_LENGTH))
    print("{:<20} {:>20}".format("BP_ENERGY_WEIGHT", BP_ENERGY_WEIGHT))
    print("{:<20} {:>20}".format("NORMALIZED_RT", NORMALIZED_RT))
    print("-" * len(header))
    print(f"Sequence: {seq}\n")


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


def create_scoring_tables(seq: str) -> tuple[np.ndarray]:
    n = len(seq) + 1
    qbp = np.zeros((n, n))
    q = np.ones((n, n))
    for i, j in np.ndindex(q.shape):
        # 1-based indexing and skipping fields below diagonal
        if j == 0 or i == 0 or i > j:
            continue
        try:
            qbp[i][j] = (
                q[i + 1][j - 1] * np.exp(-BP_ENERGY_WEIGHT / NORMALIZED_RT)
                if check_pairing(seq[i - 1], seq[j - 1])
                else 0
            )
        except IndexError:
            pass
        ks = [k for k in range(i, j) if i <= k < j - MIN_LOOP_LENGTH]
        q[i][j] = q[i][j - 1] + sum(q[i][k - 1] * qbp[k][j] for k in ks)
    return q[1:, :], qbp[1:, :]


def calc_paired_unpaired_probabilities(
    q: np.ndarray, qbp: np.ndarray
) -> np.ndarray:
    pass


if __name__ == "__main__":
    seq = argv[1]
    if not check_sequence(seq):
        print("Invalid sequence!")
        exit(1)
    print_params(seq)
    q, qbp = create_scoring_tables(seq)
    print(f"Q:\n{q.round(2)}\n")
    print(f"Qbp:\n{qbp.round(2)}\n")
