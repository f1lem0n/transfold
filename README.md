# Transfold (WIP)

## Prerequisites

- conda >= 23.5.0
- git

## Setup

Run this in your terminal (for UNIX-based systems):

1. Clone the repository and create conda environment:

```
git clone https://github.com/f1lem0n/transfold.git
cd transfold
conda env create -f environment.yaml
```

## Usage

1. Firstly `conda activate transfold`.
2. To see help execute `python transfold.py -h`.

## Development

1. Develop a feature in separate branch.
2. Use conda environment `transfold` for development or create separate env.
3. Use `make` for automated tasks:
    ```
    $ make
    help - display this help message
    test - measure code coverage with pytest
    format - format package with black and isort
    lint - static code analysis with flake8 and mypy
    clean - remove common artifacts from the directory tree
    ```
