import click
import json
from shutil import copyfile
from pathlib import Path
from typing import Any

from .constants import DEFAULTS_FILE_NAME, DOMAINS_FILE_NAME, PORTS_FILE_NAME, PROJECTS_FILE_NAME, CONFIG_DIR


@click.group('config')
def cli():
    pass


@cli.command('init')
@click.option('--rewrite', is_flag=True, default=False, type=click.BOOL)
def init(rewrite: bool):
    files = [DEFAULTS_FILE_NAME, DOMAINS_FILE_NAME,
             PORTS_FILE_NAME, PROJECTS_FILE_NAME]
    current_dir = Path('.')
    for file_name in files:
        file = CONFIG_DIR / file_name
        if rewrite or not file.exists():
            copyfile(current_dir / file_name, file,)


@cli.command('get')
@click.option('--key', type=click.STRING, required=False)
def get(key: str | None):
    if not key:
        config = json.load()
        click.echo("Not key")
        return None
    return


@cli.command('set')
@click.option('--key', type=click.STRING)
@click.option('--value')
def set(key: str, value: Any):
    pass
