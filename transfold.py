from pathlib import Path

import click
import yaml

from modules.scopes_parser import get_scope_df
from modules.downloaders import download_all_protein_sequences


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
    "get",
    context_settings=dict(ignore_unknown_options=True),
    short_help="Get data for Transfold",
)
@click.argument(
    "data",
    type=click.Choice(["coding_seq", "protein_seq", "all"]),
    default="all",
)
@click.option(
    "--scope",
    "-s",
    default=Path("data/dir.cla.scope.2.08-stable.tsv").absolute(),
    help="Path to CLA SCOPe tsv file",
)
@click.option(
    "--output",
    "-o",
    default=Path("data/").absolute(),
    help="Path to data output directory",
)
def get(data, scope, output):
    output = Path(output).absolute()
    scope_df = get_scope_df(scope)
    if data == "protein_seq":
        download_all_protein_sequences(output, scope_df)
    if data == "all":
        download_all_protein_sequences(output, scope_df)


if __name__ == "__main__":
    cli()
