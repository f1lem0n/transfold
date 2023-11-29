```
 /$$$$$$$$                                      /$$$$$$          /$$       /$$
|__  $$__/                                     /$$__  $$        | $$      | $$
   | $$  /$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$| $$  \__//$$$$$$ | $$  /$$$$$$$
   | $$ /$$__  $$|____  $$| $$__  $$ /$$_____/| $$$$   /$$__  $$| $$ /$$__  $$
   | $$| $$  \__/ /$$$$$$$| $$  \ $$|  $$$$$$ | $$_/  | $$  \ $$| $$| $$  | $$
   | $$| $$      /$$__  $$| $$  | $$ \____  $$| $$    | $$  | $$| $$| $$  | $$
   | $$| $$     |  $$$$$$$| $$  | $$ /$$$$$$$/| $$    |  $$$$$$/| $$|  $$$$$$$
   |__/|__/      \_______/|__/  |__/|_______/ |__/     \______/ |__/ \_______/
```
> A tool for predicting fold category based on transcript sequence and structure.

## Prerequisites

- conda >= 23.5.0
- git

## Setup

Stable version is not yet available. Please see [Development](#development) section.

## Usage

Upon executing `transfold` you will see the following help:

```
$ transfold
Usage: transfold [OPTIONS] COMMAND [ARGS]...

  T R A N S F O L D

  A tool for predicting fold category based on transcript sequence and
  structure.

Options:
  -v, --version  Show version
  -h, --help     Show this message and exit.

Commands:
  download  Download Transfold Database
  run       Run Transfold

```

## Development

1. Develop a feature in separate branch.
2. Setup (`conda env create -f environment.yaml`) and use conda environment `transfold` for development.
3. Use `make` for automated tasks:
   ```
   $ make help

   MAKE TARGETS ARE FOR DEVELOPMENT PURPOSES ONLY.
   PLEASE USE CONDA ENV FOR RUNNING ANY OF THE MAKE TARGETS.

   Available targets:
   help - display this help message
   test - measure code coverage with pytest
   format - format package with black and isort
   lint - static code analysis with flake8 and mypy
   clean - remove common artifacts from the directory tree as well as built and installed package
   checksum - generate md5 checksum of the repository
   verify - verify md5 checksum of the repository (if stdout is empty then checksums are equal)
   install - build and install current development version in a virtual environment
   ```
