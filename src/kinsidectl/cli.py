import click

from domain.cli import cli as domain_cli
from config.cli import cli as config_cli


@click.group()
def cli():
    pass


cli.add_command(domain_cli)
cli.add_command(config_cli)
