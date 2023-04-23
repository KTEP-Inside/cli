from typing import TypeVar
from json import dumps, loads

from .base_config_file import BaseConfigFile

_TJsonConfig = TypeVar('_TJsonConfig')


class BaseJSONConfigFile(BaseConfigFile[_TJsonConfig]):
    def _postread(self, content: str) -> _TJsonConfig:
        return loads(content)

    def _prewrite(self, config: _TJsonConfig) -> str:
        return dumps(config, indent=2)
