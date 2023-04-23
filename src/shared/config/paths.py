from typing import Final
from pathlib import Path

TEMPLATE_DIR: Final[Path] = Path("templates")
CONFIG_DIR: Final[Path] = Path.home() / Path('.kinsidectl')
DEFAULT_ENV_FILE_NAME: Final[str] = '.env'
