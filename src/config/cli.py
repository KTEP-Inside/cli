import click
import json
from shutil import copyfile
from pathlib import Path
from typing import Any

from shared.lib import write_config
from shared.config import TEMPLATE_DIR

from .lib import split_key, get_config_value, read_default_config
from .config import DEFAULT_CONFIG_NAME, CONFIG_DIR, DEFAULT_CONFIG


@click.group('config')
def cli():
    pass


@cli.command('init')
@click.option('--rewrite', is_flag=True, default=False, type=click.BOOL)
def init(rewrite: bool):
    if not Path.exists(CONFIG_DIR):
        Path.mkdir(CONFIG_DIR)
    if rewrite or not DEFAULT_CONFIG.exists():
        copyfile(TEMPLATE_DIR / DEFAULT_CONFIG_NAME, DEFAULT_CONFIG)


@cli.command('get')
@click.option('--key', type=click.STRING, required=False)
def get(key: str | None):
    if not key:
        click.echo(DEFAULT_CONFIG.read_text(), color=True)
        return

    keys = split_key(key)
    value = get_config_value(read_default_config(), keys)

    click.echo(json.dumps(value, indent=2))
    return


@cli.command('set')
@click.option('--key', type=click.STRING)
@click.option('--value')
def set(key: str, value: Any):
    keys = split_key(key)
    config = read_default_config()

    parent_keys = keys[:-1]
    target_key = keys[-1]
    target_section = get_config_value(config, parent_keys)

    target_section[target_key] = value

    write_config(DEFAULT_CONFIG, config)
