from typing import List, Callable, Any, Dict
from pathlib import Path
from json import loads

from .constants import CONFIG_DIR


def split_key(key: str) -> List[str]:
    return key.split('.')


def get_config(file: Path) -> Dict:
    return loads(file.read_text())


def get_config_value(config: Dict, keys: List[str]) -> Any | None:
    value = config
    for key in keys:
        if key.isdigit():
            key = int(key)
        value = value.get(key)

        if not value:
            return None

    return value


def with_config_file(name: str) -> Callable:
    path = CONFIG_DIR / name

    def wrapper(func: Callable):
        def foo(*args, **kwargs):
            return func(path, *args, **kwargs)
        return foo
    return wrapper
