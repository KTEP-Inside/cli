from typing import Final
from pathlib import Path

from ...config import CONFIG_DIR


DEFAULT_CONFIG_NAME: Final[str] = 'default.json'
DEFAULT_CONFIG: Final[Path] = CONFIG_DIR / DEFAULT_CONFIG_NAME
