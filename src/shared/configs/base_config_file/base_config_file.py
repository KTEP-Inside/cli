from abc import ABC
from typing import TypeVar,  Generic
from pathlib import Path
from os import remove

_TConfig = TypeVar('_TConfig')


class BaseConfigFile(Generic[_TConfig], ABC):
    path: Path
    config: _TConfig

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.read()

    def read(self, path: Path | None = None):
        _path = path or self.path
        self.path = _path
        self.config = self._postread(self.path.read_text())

    def save(self, path: Path | None = None):
        _path = path or self.path
        _path.write_text(self._prewrite(self.config))

    def remove(self):
        remove(self.path)
        self.path = None

    def _postread(self, content: str) -> _TConfig:
        return content

    def _prewrite(self, config: _TConfig) -> str:
        return config
