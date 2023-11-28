from pathlib import Path

import click
import yaml

from modules.downloaders import cds_downloader
from modules.scope_parser import get_scope_df


def read_yaml_file(filepath):
    with open(Path(filepath).absolute(), "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    """
    Transfold
    """


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
    short_help="Get data for Transfold",
)
@click.option(
    "--scope",
    "-s",
    default=Path("data/dir.cla.scope.2.08-stable.tsv").absolute(),
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
    default=Path("data/").absolute(),
    help="Path to data output directory",
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
def download(scope, output, pattern, retries, timeout):
    output = Path(output).absolute()
    scope_df = get_scope_df(scope, pattern)
    cds_downloader(scope_df, output, retries, timeout)


if __name__ == "__main__":
    cli()
