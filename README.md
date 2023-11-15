# msc (WIP)

## Prerequisites

- conda >= 23.5.0
- git

## Setup

Run this in your terminal (for UNIX-based systems):

```
git clone https://github.com/f1lem0n/msc.git
cd msc
conda env create -f envs/msc.yaml -y
```

## Usage

1. Firstly `conda activate msc`.
2. Run `python3 scripts/mccaskill.py <RNA_sequence>`

## Development

1. Develop a feature in separate branch.
2. Use conda environment `msc` for development or create separate env.
3. Use `make` for automated tasks:
    ```
    $ make
    help - display this help message
    test - measure code coverage with pytest
    format - format package with black
    lint - static code analysis with flake8 and mypy
    clean - remove common artifacts from the directory tree
    ```