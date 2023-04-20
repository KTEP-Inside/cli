import click

from domain.cli import cli as domain_cli
from config import config_cli
from project import project_cli


@click.group()
def cli():
    pass


cli.add_command(domain_cli)
cli.add_command(config_cli)
cli.add_command(project_cli)
