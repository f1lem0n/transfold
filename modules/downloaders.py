from pathlib import Path

import pandas as pd
from tqdm import tqdm

from modules.scopes_parser import get_pdb_ids, get_protein_sequence


def download_all_protein_sequences(
    output: Path, scope_df: pd.DataFrame
) -> int:
    if not (output / "protein_seq").exists():
        (output / "protein_seq").mkdir(parents=True)
    pdb_ids = get_pdb_ids(scope_df)
    skipped = 0
    for pdb_id in tqdm(pdb_ids):
        if (output / "protein_seq" / f"{pdb_id}.fasta").exists():
            continue
        sequence = get_protein_sequence(pdb_id)
        if not sequence:
            skipped += 1
            continue
        with open(output / "protein_seq" / f"{pdb_id}.fasta", "w") as file:
            file.write(f">{pdb_id}\n{sequence}")
    return skipped


# def download_all_coding_sequences(
#         output: Path, scope_df: pd.DataFrame
# ) -> int:
#     pass
