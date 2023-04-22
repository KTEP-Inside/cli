from abc import ABC
from typing import TypeVar,  Generic, Dict
from pathlib import Path
from os import remove
from json import dumps, loads

_TCONFIG = TypeVar('_TCONFIG', bound=Dict)


class BaseConfigFile(Generic[_TCONFIG], ABC):
    _path: Path
    config: _TCONFIG

    def __init__(self, path: str | Path):
        self._path = Path(path)
        self.read()

    def read(self, path: Path | None = None):
        _path = path or self._path
        self._path = _path
        self.config = loads(self._path.read_text())

    def save(self, path: Path | None = None):
        _path = path or self._path
        _path.write_text(self._formate())

    def remove(self):
        remove(self._path)
        self._path = None

    def _formate(self) -> str:
        return dumps(self.config, indent=2)
