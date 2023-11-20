import shutil
import subprocess
from pathlib import Path

from pandas import DataFrame
from tqdm import tqdm

from modules.scope_parser import (
    get_category,
    get_gene_id,
    get_pdb_ids,
    get_uniprot_id,
)


def cds_downloader(
    scope_df: DataFrame, output: Path, retries: int, timeout: int
) -> int:
    pdb_ids = get_pdb_ids(scope_df)
    for pdb_id in tqdm(pdb_ids):
        category = get_category(scope_df, pdb_id)
        try:
            gene_id = get_gene_id(
                get_uniprot_id(pdb_id, retries, timeout), retries, timeout
            )
        except Exception:
            gene_id = ""

        # skip if dir already exists or gene_id is not found
        if not gene_id:
            continue
        if (output / "CDS" / category / pdb_id).exists():
            continue

        # if temp folder exists delete it and create a new one
        if (output / "temp").exists():
            shutil.rmtree(output / "temp")
        (output / "temp").mkdir(parents=True)

        # download and unzip data from NCBI
        subprocess.run(
            f'curl -X GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/id/{gene_id}/download?include_annotation_type=FASTA_GENE&table_fields=gene-id&table_fields=gene-type&table_fields=description" -o {str(output / "temp" / pdb_id)}.zip',
            capture_output=True,
            shell=True,
        )
        subprocess.run(
            f"unzip {str(output / 'temp' / pdb_id)}.zip -d {output / 'temp'}",
            capture_output=True,
            shell=True,
        )

        # move data to categorized CDS folder
        (output / "CDS" / category / pdb_id).mkdir(parents=True)
        shutil.move(
            output / "temp" / "ncbi_dataset" / "data",
            output / "CDS" / category / pdb_id,
            copy_function=shutil.copytree,
        )

        # clean up temp folder
        shutil.rmtree(output / "temp")
