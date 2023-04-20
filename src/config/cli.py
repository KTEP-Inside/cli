import click
import json
from shutil import copyfile
from pathlib import Path
from typing import Any

from .lib import split_key, get_config_value, read_config, write_config
from .constants import DEFAULTS_FILE_NAME, CONFIG_DIR, TEMPLATE_DIR, DEFAULTS_FILE


@click.group('config')
def cli():
    pass


@cli.command('init')
@click.option('--rewrite', is_flag=True, default=False, type=click.BOOL)
def init(rewrite: bool):
    Path.mkdir(CONFIG_DIR)
    if rewrite or not DEFAULTS_FILE.exists():
        copyfile(TEMPLATE_DIR / DEFAULTS_FILE_NAME, DEFAULTS_FILE)


@cli.command('get')
@click.option('--key', type=click.STRING, required=False)
def get(key: str | None):
    if not key:
        click.echo(DEFAULTS_FILE.read_text(), color=True)
        return

    keys = split_key(key)
    value = get_config_value(read_config(DEFAULTS_FILE), keys)

    click.echo(json.dumps(value, indent=2))
    return


@cli.command('set')
@click.option('--key', type=click.STRING)
@click.option('--value')
def set(key: str, value: Any):
    keys = split_key(key)
    config = read_config(DEFAULTS_FILE)

    parent_keys = keys[:-1]
    target_key = keys[-1]
    target_section = get_config_value(config, parent_keys)

    target_section[target_key] = value

    write_config(DEFAULTS_FILE, config)
