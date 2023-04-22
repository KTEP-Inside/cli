from typing import Final
from pathlib import Path

from ...config import CONFIG_DIR


DOMAINS_CONFIG_NAME: Final[str] = 'domains.json'
DOMAINS_CONFIG: Final[Path] = CONFIG_DIR / DOMAINS_CONFIG_NAME
