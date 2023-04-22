import click
from json import dumps
from shutil import copyfile
from typing import Any

from shared.config import TEMPLATE_DIR, CONFIG_DIR
from shared.configs.default import DefaultConfigFile, DEFAULT_CONFIG_NAME, DEFAULT_CONFIG

from .lib import split_key, get_config_value


@click.group('config')
def cli():
    pass


@cli.command('init')
@click.option('--rewrite', is_flag=True, default=False, type=click.BOOL)
def init(rewrite: bool):
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    if rewrite or not DEFAULT_CONFIG.exists():
        copyfile(TEMPLATE_DIR / DEFAULT_CONFIG_NAME, DEFAULT_CONFIG)


@cli.command('get')
@click.option('--key', type=click.STRING, required=False)
def get(key: str | None):
    default_config_file = DefaultConfigFile()
    default_config = default_config_file.config

    if not key:
        click.echo(default_config, color=True)
        return

    keys = split_key(key)
    value = get_config_value(default_config, keys)

    click.echo(dumps(value, indent=2))


@cli.command('set')
@click.option('--key', type=click.STRING)
@click.option('--value')
def set(key: str, value: Any):
    keys = split_key(key)
    default_config_file = DefaultConfigFile()

    parent_keys = keys[:-1]
    target_key = keys[-1]
    target_section = get_config_value(default_config_file.config, parent_keys)

    target_section[target_key] = value

    default_config_file.save()
