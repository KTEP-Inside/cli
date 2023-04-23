from typing import TypeVar
from json import dumps, loads

from .base_config_file import BaseConfigFile

_TJsonConfig = TypeVar('_TJsonConfig')


class BaseJSONConfigFile(BaseConfigFile[_TJsonConfig]):
    def _postread(self) -> None:
        self.config = loads(self._raw)

    def _prewrite(self) -> None:
        self._raw = dumps(self.config, indent=2)
