from typing import Tuple, Any

from .config import INJECT_BLACKLIST


def filter_injected_keys(pair: Tuple[str, Any]) -> bool:
    return pair[0] not in INJECT_BLACKLIST
