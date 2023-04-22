from typing import Any, TypeVar, Dict

_KT = TypeVar('_KT', bound=Any)
_VT = TypeVar('_VT', bound=Any)


def get_or_create(d: Dict[_KT, _VT], key: _KT, value: _VT) -> _VT:
    v = d.get(key)

    if v:
        return v
    d[key] = value
    return value
