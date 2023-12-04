import logging
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from pandas import DataFrame
from tqdm import tqdm

from transfold.modules.scope_parser import (
    get_category,
    get_gene_id,
    get_pdb_ids,
    get_uniprot_id,
)


class Writeable:  # pragma: no cover
    @staticmethod
    def download_sequence_data():
        ...

    @staticmethod
    def download_all_sequence_data():
        ...


def download_sequence_data(
    pdb_id: str,
    scope_df: DataFrame,
    output: Path,
    retries: int,
    timeout: int,
    logger: logging.Logger,
) -> Writeable | None:
    # skip if dir already exists or uniprot_id or gene_id is not found
    category = get_category(scope_df, pdb_id, logger)
    if (output / "sequence_data" / category / pdb_id).exists():
        logger.debug(f"Skipping {pdb_id} as it already exists")
        return None
    uniprot_id = get_uniprot_id(pdb_id, retries, timeout, logger)
    if not uniprot_id:
        return None
    gene_id = get_gene_id(uniprot_id, retries, timeout, logger)
    if not gene_id:
        return None
    # if temp folder exists delete it and create a new one
    (output / "temp").mkdir(parents=True, exist_ok=True)
    # download and unzip data from NCBI
    logger.debug("Downloading archive")
    subprocess.run(
        'curl -X GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/'
        f"id/{gene_id}/download?include_annotation_type=FASTA_GENE"
        "&include_annotation_type=FASTA_CDS"
        '&include_annotation_type=FASTA_RNA"'
        f' -o {str(output / "temp" / pdb_id)}.zip',
        capture_output=True,
        shell=True,
    )
    if not is_zipfile(f"{output / 'temp' / pdb_id}.zip"):  # pragma: no cover
        return None
    logger.debug("Unzipping archive")
    with ZipFile(f"{output / 'temp' / pdb_id}.zip", "r") as zip_ref:
        zip_ref.extractall(output / "temp" / pdb_id)
    # move data to categorized sequence_data folder
    logger.debug(
        f"Moving data to: {output / 'sequence_data' / category / pdb_id}"
    )
    (output / "sequence_data" / category / pdb_id).mkdir(parents=True)
    shutil.move(
        output / "temp" / pdb_id / "ncbi_dataset" / "data",
        output / "sequence_data" / category / pdb_id,
        copy_function=shutil.copytree,
    )
    if (output / "temp" / pdb_id).exists():
        shutil.rmtree(output / "temp" / pdb_id)
    return Writeable()


def download_all_sequence_data(
    scope_df: DataFrame,
    output: Path,
    jobs: int,
    retries: int,
    timeout: int,
    logger: logging.Logger,
    verbose=False,
) -> Writeable:
    logger.info(f"Starting sequence data download at: {output}")
    logger.info(
        f"PARAMS:\n"
        f"\n\tretries: {retries}"
        f"\n\ttimeout: {timeout}"
        f"\n\tconcurrent jobs: {jobs}\n"
    )
    pdb_ids = get_pdb_ids(scope_df, logger)
    with ProcessPoolExecutor(max_workers=jobs) as executor:
        with tqdm(total=len(pdb_ids)) as progress:
            # both futures and results lists are needed for the progress bar
            futures = []
            for pdb_id in pdb_ids:
                future = executor.submit(
                    download_sequence_data,
                    pdb_id,
                    scope_df,
                    output,
                    retries,
                    timeout,
                    logger,
                )
                future.add_done_callback(lambda _: progress.update())
                futures.append(future)
            results = []
            for future in futures:
                result = future.result()
                results.append(result)

    logger.info("Sequence data download complete\n")
    return Writeable()
