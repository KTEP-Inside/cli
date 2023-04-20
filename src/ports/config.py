from typing import Final
from pathlib import Path

from shared.config import CONFIG_DIR

PORTS_CONFIG_NAME: Final[str] = 'ports.json'
PORTS_CONFIG: Final[Path] = CONFIG_DIR / PORTS_CONFIG_NAME
