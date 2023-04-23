from typing import \
    Iterable, Sequence,\
    Any, Mapping
from re import match
from ..base_config_file import BaseConfigFile

from .lib import create_key
from .types import _EnvDict
from .config import PRIMITIVES, PATTERN


class EnvConfigFile(BaseConfigFile[_EnvDict]):
    def update(self, source: Iterable, key_prefix: str | None = None):
        if isinstance(source, Mapping):
            return self._update_env_dict_by_mapping(source, key_prefix)
        elif isinstance(source, Sequence):
            return self._update_env_dict_by_sequence(source, key_prefix)
        raise TypeError(
            f"Тип {type(source).__name__} не поддерживается. Используйте типы производные от {Mapping.__name__} и {Sequence.__name__}.")

    def _prewrite(self):
        result = ""

        for key, value in self.config.items():
            if type(value) is bool:
                value = int(value)
            result += PATTERN.format(key=key, value=value)

        self._raw = result

    def _postread(self) -> None:
        result = {}

        for line in self._raw.split('\n'):
            if line.startswith('#') or not line.strip():
                continue

            key, value, = line.split('=')

            if value.isdigit():
                value = int(value)
            elif match(r"(\$\{.+\})", value):
                value = value.replace("${", "{")
                value = value.format_map(result)
            result[key] = value

        self.config = result

    def _update_env_dict_by_mapping(self, source: Mapping[str, Any], key_prefix: str | None = None):
        for key in source:
            self._update_env_dict(str(key), source[key], key_prefix)

    def _update_env_dict_by_sequence(self, source: Sequence[Any], key_prefix: str | None = None) -> str:
        for key, value in enumerate(source):
            self._update_env_dict(str(key), value, key_prefix)

    def _update_env_dict(self, key: str, value: Any, key_prefix: str | None = None):
        value_type = type(value)
        target_key = create_key(key, key_prefix)

        if value_type in PRIMITIVES:
            self.config[target_key] = value

        elif isinstance(value, Mapping):
            self._update_env_dict_by_mapping(value,  target_key)

        elif isinstance(value, Sequence):
            self._update_env_dict_by_sequence(value,  target_key)
