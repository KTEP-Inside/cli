from typing import Final
from pathlib import Path

from shared.config import CONFIG_DIR


DEFAULT_CONFIG_NAME: Final[str] = 'default.json'
DOMAINS_CONFIG_NAME: Final[str] = 'domains.json'


DEFAULT_CONFIG: Final[Path] = CONFIG_DIR / DEFAULT_CONFIG_NAME
DOMAINS_CONFIG: Final[Path] = CONFIG_DIR / DOMAINS_CONFIG_NAME
