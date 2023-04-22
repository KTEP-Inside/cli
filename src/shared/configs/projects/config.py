from typing import Final
from pathlib import Path

from ...config import CONFIG_DIR

PROJECTS_CONFIG_NAME: Final[str] = 'projects.json'
PROJECT_CONFIG_NAME: Final[str] = '.kinsiderc'

PROJECTS_CONFIG: Final[Path] = CONFIG_DIR / PROJECTS_CONFIG_NAME
