from typing import \
    Dict, Iterable, \
    Final, List, Sequence,\
    Any, Mapping
from re import match

from .types import _EnvDict

_PATTERN = "{key}={value}\n"


COMPLEX_KEY_PATTERN = '{prefix}_{base}'


def dict_to_env_str(d: Dict, prefix: str | None = None) -> str:
    result = ""
    for key, value in d.items():

        if type(value) is bool:
            value = int(value)
        result += _PATTERN.format(key=_get_key(key, prefix), value=value)

    return result


PRIMITIVES: Final[List] = [int, float, bool, str]


def update_env_dict(source: Iterable, target: _EnvDict, key_prefix: str | None = None) -> str:
    if isinstance(source, Mapping):
        return _update_env_dict_by_mapping(source, target, key_prefix)
    elif isinstance(source, Sequence):
        return _update_env_dict_by_sequence(source, target, key_prefix)

    raise TypeError(
        f"Тип {type(source).__name__} не поддерживается. Используйте типы производные от {Mapping.__name__} и {Sequence.__name__}.")


def _update_env_dict_by_mapping(source: Mapping[str, Any],
                                target: _EnvDict, key_prefix: str | None = None) -> str:
    for key in source:
        value = source[key]
        _update_env_dict(str(key), value, target, key_prefix)


def _update_env_dict_by_sequence(source: Sequence[Any], target: _EnvDict, key_prefix: str | None = None) -> str:
    for key, value in enumerate(source):
        _update_env_dict(str(key), value, target, key_prefix)


def _update_env_dict(key: str, value: Any, target: _EnvDict, key_prefix: str | None = None):
    value_type = type(value)
    target_key = _get_key(key, key_prefix)

    if value_type in PRIMITIVES:
        target[target_key] = value
    elif isinstance(value, Mapping):
        _update_env_dict_by_mapping(value, target, target_key)
    elif isinstance(value, Sequence):
        _update_env_dict_by_sequence(value, target, target_key)


def _get_key(base: str, prefix: str | None = None) -> str:
    key = base.upper()
    if prefix:
        key = COMPLEX_KEY_PATTERN.format(prefix=prefix.upper(), base=key)

    return key


def env_str_to_dict(env: str) -> Dict:
    result = {}

    for line in env.split('\n'):
        if line.startswith('#') or not line.strip():
            continue

        key, value, = line.split('=')

        if value.isdigit():
            value = int(value)
        elif match(r"(\$\{.+\})", value):
            value = value.replace("${", "{")
            value = value.format_map(result)
        result[key] = value

    return result
