from abc import ABC
from typing import TypeVar,  Generic
from pathlib import Path
from os import remove

_TConfig = TypeVar('_TConfig')


class BaseConfigFile(Generic[_TConfig], ABC):
    path: Path
    config: _TConfig
    _raw: str

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.read()

    def read(self, path: Path | None = None) -> None:
        _path = path or self.path
        self.path = _path
        self._raw = self.path.read_text()
        self._postread()

    def save(self, path: Path | None = None) -> None:
        _path = path or self.path
        self._prewrite()
        _path.write_text(self._raw)

    def remove(self) -> None:
        remove(self.path)
        self.path = None

    def _postread(self) -> None:
        self.config = self._raw

    def _prewrite(self) -> None:
        self._raw = str(self.config)
