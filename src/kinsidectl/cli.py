import click

from domain import domains_cli
from config import config_cli
from ports import ports_cli
from project import project_cli


@click.group()
def cli():
    pass


cli.add_command(domains_cli)
cli.add_command(config_cli)
cli.add_command(ports_cli)
cli.add_command(project_cli)
