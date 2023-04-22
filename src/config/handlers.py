from click import echo
from json import dumps
from typing import Any
from shutil import copyfile

from shared.config import CONFIG_DIR, TEMPLATE_DIR
from shared.configs.default import \
    DEFAULT_CONFIG, DEFAULT_CONFIG_NAME, \
    DefaultConfigFile

from .lib import split_key, get_config_value


def init(rewrite: bool):
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()

    if rewrite or not DEFAULT_CONFIG.exists():
        copyfile(TEMPLATE_DIR / DEFAULT_CONFIG_NAME, DEFAULT_CONFIG)


def get(key: str | None):
    default_config_file = DefaultConfigFile()
    default_config = default_config_file.config

    if not key:
        echo(default_config, color=True)
        return

    keys = split_key(key)
    value = get_config_value(default_config, keys)

    echo(dumps(value, indent=2))


def set(key: str, value: Any):
    default_config_file = DefaultConfigFile()

    keys = split_key(key)
    parent_keys = keys[:-1]
    target_key = keys[-1]
    target_section = get_config_value(default_config_file.config, parent_keys)

    target_section[target_key] = value

    default_config_file.save()
