import click
import json
from shutil import copyfile
from pathlib import Path
from typing import Any

from .lib import with_config_file, split_key, get_config_value, get_config
from .constants import DEFAULTS_FILE_NAME, DOMAINS_FILE_NAME, PORTS_FILE_NAME, PROJECTS_FILE_NAME, CONFIG_DIR, TEMPLATE_DIR, DEFAULTS_FILE


@click.group('config')
def cli():
    pass


@cli.command('init')
@click.option('--rewrite', is_flag=True, default=False, type=click.BOOL)
def init(rewrite: bool):
    files = [DEFAULTS_FILE_NAME, DOMAINS_FILE_NAME,
             PORTS_FILE_NAME, PROJECTS_FILE_NAME]
    for file_name in files:
        file = CONFIG_DIR / file_name
        if rewrite or not file.exists():
            copyfile(TEMPLATE_DIR / file_name, file,)


@cli.command('get')
@click.option('--key', type=click.STRING, required=False)
@with_config_file(DEFAULTS_FILE_NAME)
def get(file: Path, key: str | None):
    if not key:
        click.echo(file.read_text(), color=True)
        return
    
    keys = split_key(key)
    value = get_config_value(get_config(file), keys)

    click.echo(json.dumps(value, indent=2))
    return


@cli.command('set')
@click.option('--key', type=click.STRING)
@click.option('--value')
@with_config_file(DEFAULTS_FILE_NAME)
def set(file: Path, key: str, value: Any):
    keys = split_key(key)
    config = get_config(file)

    parent_keys = keys[:-1]    
    target_key = keys[-1]
    target_section = get_config_value(config, parent_keys)
    
    target_section[target_key] = value
    
    DEFAULTS_FILE.write_text(json.dumps(config))