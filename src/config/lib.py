from typing import List, Any, Dict

def split_key(key: str) -> List[str]:
    return key.split('.')


def get_config_value(config: Dict, keys: List[str]) -> Any | None:
    value = config
    for key in keys:
        if key.isdigit():
            key = int(key)
        value = value.get(key)

        if not value:
            return None

    return value
