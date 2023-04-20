from typing import List, Callable, Any, Dict
from pathlib import Path
from json import loads, dumps

from .constants import CONFIG_DIR


def split_key(key: str) -> List[str]:
    return key.split('.')


def read_config(file: Path) -> Dict:
    return loads(file.read_text())


def write_config(file: Path, content: Any) -> None:
    return file.write_text(dumps(content, indent=2))


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
