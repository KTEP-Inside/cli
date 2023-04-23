from ..base_config_file import BaseConfigFile

from .lib import dict_to_env_str, env_str_to_dict
from .types import _EnvDict


class EnvConfigFile(BaseConfigFile[_EnvDict]):
    def _prewrite(self, config: _EnvDict) -> str:
        return dict_to_env_str(config)

    def _postread(self, content: str) -> _EnvDict:
        return env_str_to_dict(content)
