from typing import List, Any, Dict

from shared.lib import read_config

from .types import DefaultConfig
from .config import DEFAULT_CONFIG


def split_key(key: str) -> List[str]:
    return key.split('.')


def get_config_value(config: Dict, keys: List[str]) -> Any | None:
    value = config
    for key in keys:
        if key.isdigit():
            key = int(key)
        value = value.get(key)

        if not value:
            return None

    return value


def read_default_config() -> DefaultConfig:
    return read_config(DEFAULT_CONFIG)
