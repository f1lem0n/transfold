import logging
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from zipfile import ZipFile, is_zipfile

import pandas as pd
import requests as rq
from tqdm import tqdm


class Writeable:  # pragma: no cover
    ...


class SequenceDataDownloader:
    """
    Downloads sequence data from NCBI for PDB IDs in SCOPe file.\n
    Paralleling here is done using ProcessPoolExecutor.\n
    """

    def __init__(
        self,
        scope_path: Path,
        pattern: str,
        output: Path,
        retries: int,
        timeout: int,
        jobs: int,
        logger: logging.Logger,
        verbose=False,
        name="SequenceDataDownloader",
    ) -> None:
        self.name = name
        self.scope_path = scope_path
        self.pattern = pattern
        self.output = output
        self.logger = logger
        self.retries = retries
        self.timeout = timeout
        self.verbose = verbose
        self.jobs = jobs
        self.scope_df = self._get_scope_df()
        self.pdb_ids = self._get_pdb_ids()

    def _get_scope_df(self) -> pd.DataFrame:
        self.logger.info(f"Reading SCOPe file: {self.scope_path}")
        scope_df = pd.read_table(
            self.scope_path,
            sep="\t",
            header=None,
            names=[
                "scope_id",
                "pdb_id",
                "chain",
                "category",
                "NA1",
                "NA2",
            ],
        )
        self.logger.info(
            f"Filtering SCOPe file by category pattern: {self.pattern}"
        )
        scope_df = scope_df[
            scope_df["category"].str.contains(
                self.pattern,
                regex=True,
                na=False,
            )
        ]
        return scope_df

    def _get_category(self, pdb_id: str) -> str:
        try:
            cat = self.scope_df[self.scope_df["pdb_id"] == pdb_id][
                "category"
            ].tolist()[0]
            self.logger.debug(f"Category for {pdb_id}: {cat}")
            return cat
        except (KeyError, IndexError):
            self.logger.error(f"Category for {pdb_id} not found")
            return ""

    def _get_uniprot_id(
        self,
        pdb_id: str,
    ) -> str:
        for _ in range(self.retries):
            try:
                response = rq.get(
                    "https://data.rcsb.org/rest/"
                    f"v1/core/polymer_entity/{pdb_id}/1",
                    timeout=self.timeout,
                )
            except Exception:  # pragma: no cover
                self.logger.warning("Connection timeout. Retrying...")
                continue
            if response.status_code == 200:
                self.logger.debug("Connected to PDB")
                content = response.json()
                response.close()
                try:
                    uniprot_id = content[
                        "rcsb_polymer_entity_container_identifiers"
                    ]["uniprot_ids"][0]
                    self.logger.debug(
                        f"Found UniProt ID for {pdb_id}: {uniprot_id}"
                    )
                except KeyError:  # pragma: no cover
                    self.logger.error(f"UniProt ID for {pdb_id} not found")
                    return ""
                return uniprot_id.upper()
        self.logger.error("Connection error. Exceeded retries")
        return ""

    def _get_gene_id(
        self,
        uniprot_id: str,
    ) -> str:
        for _ in range(self.retries):
            try:
                response = rq.get(
                    f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.txt",
                    timeout=self.timeout,
                )
            except Exception:  # pragma: no cover
                self.logger.warning("Connection timeout. Retrying...")
                continue
            if response.status_code == 200:
                self.logger.debug("Connected to UniProt")
                content = response.text.split("\n")
                response.close()
                for line in content:
                    if "GeneID;" in line:
                        gene_id = line.split(";")[1].strip()
                        self.logger.debug(
                            f"Found GeneID for {uniprot_id}: {gene_id}"
                        )
                        return gene_id
                self.logger.error(f"GeneID for {uniprot_id} not found")
                return ""
        self.logger.error("Connection error. Exceeded retries")
        return ""

    def _get_pdb_ids(self) -> list[str]:
        self.logger.info("Getting unique PDB IDs from SCOPe file")
        return self.scope_df["pdb_id"].unique().tolist()

    def _download_sequence_data(
        self,
        pdb_id: str,
    ) -> Writeable | None:
        # skip if dir already exists or uniprot_id or gene_id is not found
        category = self._get_category(pdb_id)
        if (self.output / category / pdb_id).exists():
            self.logger.debug(f"Skipping {pdb_id} as it already exists")
            return None
        uniprot_id = self._get_uniprot_id(pdb_id)
        if not uniprot_id:
            return None
        gene_id = self._get_gene_id(uniprot_id)
        if not gene_id:
            return None
        # if temp folder exists delete it and create a new one
        (self.output / "temp").mkdir(parents=True, exist_ok=True)
        # download and unzip data from NCBI
        self.logger.debug("Downloading archive")
        subprocess.run(
            'curl -X GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/'
            f"id/{gene_id}/download?include_annotation_type=FASTA_GENE"
            "&include_annotation_type=FASTA_CDS"
            '&include_annotation_type=FASTA_RNA"'
            f' -o {str(self.output / "temp" / pdb_id)}.zip',
            capture_output=True,
            shell=True,
        )
        if not is_zipfile(
            f"{self.output / 'temp' / pdb_id}.zip"
        ):  # pragma: no cover
            return None
        self.logger.debug("Unzipping archive")
        with ZipFile(f"{self.output / 'temp' / pdb_id}.zip", "r") as zip_ref:
            zip_ref.extractall(self.output / "temp" / pdb_id)
        # move data to categorized sequence_data folder
        self.logger.debug(
            "Moving data to: " f"{self.output / category / pdb_id}"
        )
        (self.output / category / pdb_id).mkdir(parents=True)
        shutil.move(
            self.output / "temp" / pdb_id / "ncbi_dataset" / "data",
            self.output / category / pdb_id,
            copy_function=shutil.copytree,
        )
        if (self.output / "temp" / pdb_id).exists():
            shutil.rmtree(self.output / "temp" / pdb_id)
        if (self.output / "temp" / f"{pdb_id}.zip").exists():
            (self.output / "temp" / f"{pdb_id}.zip").unlink()
        return Writeable()

    def start(
        self,
    ) -> Writeable:
        self.logger.info(f"Starting sequence data download at: {self.output}")
        self.logger.info(
            f"PARAMS:\n"
            f"\n\tRetries: {self.retries}"
            f"\n\tTimeout: {self.timeout}"
            f"\n\tConcurrent jobs: {self.jobs}\n"
        )
        with ProcessPoolExecutor(max_workers=self.jobs) as executor:
            if not self.verbose:
                with tqdm(total=len(self.pdb_ids)) as progress:
                    # both futures and results lists
                    # are needed for the progress bar
                    futures = []
                    for pdb_id in self.pdb_ids:
                        future = executor.submit(
                            self._download_sequence_data, pdb_id
                        )
                        future.add_done_callback(lambda _: progress.update())
                        futures.append(future)
                    results = []
                    for future in futures:
                        result = future.result()
                        results.append(result)
            else:
                for pdb_id in self.pdb_ids:
                    executor.submit(self._download_sequence_data, pdb_id)
        self.logger.info("Sequence data download complete\n")
        return Writeable()
