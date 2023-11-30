import io
from pathlib import Path
from time import localtime, strftime

import click
import yaml
from rich.console import Console

# from transfold._version import __version__
# from transfold.modules.downloaders import cds_downloader
# from transfold.modules.logger import get_logger
# from transfold.modules.scope_parser import get_scope_df


ASCII = r"""
 /$$$$$$$$                                      /$$$$$$          /$$       /$$
|__  $$__/                                     /$$__  $$        | $$      | $$
   | $$  /$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$| $$  \__//$$$$$$ | $$  /$$$$$$$
   | $$ /$$__  $$|____  $$| $$__  $$ /$$_____/| $$$$   /$$__  $$| $$ /$$__  $$
   | $$| $$  \__/ /$$$$$$$| $$  \ $$|  $$$$$$ | $$_/  | $$  \ $$| $$| $$  | $$
   | $$| $$      /$$__  $$| $$  | $$ \____  $$| $$    | $$  | $$| $$| $$  | $$
   | $$| $$     |  $$$$$$$| $$  | $$ /$$$$$$$/| $$    |  $$$$$$/| $$|  $$$$$$$
   |__/|__/      \_______/|__/  |__/|_______/ |__/     \______/ |__/ \_______/
"""


class RichGroup(click.Group):
    def format_help(self, ctx, formatter):
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        console.print(f"[bold magenta]{ASCII}[/bold magenta]")
        console.print(
            "[bold green]A tool for predicting fold category "
            "based on transcript sequence and structure.[/bold green]"
        )
        # [blue]Commands:[/blue]
        #     download  Download Transfold Database
        #     run       Run Transfold
        #             """
        #         )
        console.print(f"\n\n[bold yellow]{self.get_usage(ctx)}[/bold yellow]")
        console.print(
            "\n[bold yellow]To display "
            "help message for a command, run:"
            "\n\n\ttransfold COMMAND -h[/bold yellow]"
        )
        console.print("\n[cyan]Options:[/cyan]")
        for param in self.get_params(ctx):
            console.print(
                f"\t{param.get_help_record(ctx)[0]:<25}"
                f"{'[ ' + str(param.get_default(ctx)) + ' ]':<15}"
                f"{param.get_help_record(ctx)[1]:<40}"
            )

        console.print("\n[blue]Commands:[/blue]")
        for cmd_name in self.list_commands(ctx):
            cmd = self.get_command(ctx, cmd_name)
            console.print(f"\t{cmd_name:<40}{cmd.get_short_help_str(ctx):<40}")
        console.print("\n")
        formatter.write(sio.getvalue())


def read_yaml_file(filepath):
    with open(Path(filepath).absolute(), "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)


@click.group(
    cls=RichGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.option("--version", "-v", is_flag=True, help="Show version")
def cli(version):
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
