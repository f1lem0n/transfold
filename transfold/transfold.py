from pathlib import Path
from time import localtime, strftime

import click
import yaml

from transfold._version import __version__
from transfold.modules.downloaders import cds_downloader
from transfold.modules.logger import get_logger
from transfold.modules.scope_parser import get_scope_df


def read_yaml_file(filepath):
    with open(Path(filepath).absolute(), "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)


@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.option("--version", "-v", is_flag=True, help="Show version")
def cli(version):
    """
    T R A N S F O L D

    A tool for predicting fold category based on transcript sequence
    and structure.
    """
    if version:
        print(f"transfold version: {__version__}")


@cli.command(
    "run",
    context_settings=dict(ignore_unknown_options=True),
    short_help="Run Transfold",
)
def run():
    pass


@cli.command(
    "download",
    context_settings=dict(ignore_unknown_options=True),
    short_help="Download Transfold Database",
)
@click.option(
    "--scope",
    "-s",
    default=Path(__file__).parent.absolute()
    / "data"
    / "dir.cla.scope.2.08-stable.tsv",
    help="Path to CLA SCOPe tsv file",
)
@click.option(
    "--pattern",
    "-p",
    default=".*",
    help="RegExp pattern for SCOPe category",
)
@click.option(
    "--output",
    "-o",
    default=Path(__file__).parent.absolute() / "data",
    help="Path to data output directory",
)
@click.option(
    "--log",
    "-l",
    default=Path(".").absolute() / "logs",
    help="Path to logs output directory",
)
@click.option(
    "--retries",
    "-r",
    default=3,
    help="Number of retries for single HTTP request",
)
@click.option(
    "--timeout",
    "-t",
    default=10,
    help="Timeout for single HTTP request in seconds",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Print debug messages to stdout",
)
def download(scope, pattern, output, log, retries, timeout, verbose):
    start_time = strftime(r"%Y-%m-%d_%H%M%S", localtime())
    logger = get_logger(Path(log).absolute(), "download", start_time, verbose)
    scope_df = get_scope_df(scope, pattern, logger)
    output = Path(output).absolute()
    cds_downloader(scope_df, output, retries, timeout, logger, verbose)


if __name__ == "__main__":
    cli()
