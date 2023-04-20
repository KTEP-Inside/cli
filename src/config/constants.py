from typing import Final
from pathlib import Path

CONFIG_DIR: Final[Path] = Path('/etc/kinsidectl')

DEFAULTS_FILE_NAME: Final[str] = 'default.json'
DOMAINS_FILE_NAME: Final[str] = 'domains.json'
PORTS_FILE_NAME: Final[str] = 'ports.json'
PROJECTS_FILE_NAME: Final[str] = 'projects.json'
PROJECT_FILE_NAME:Final[str] = '.kinsiderc'

TEMPLATE_DIR: Final[Path] = Path('/'.join(('.', 'templates')))

DEFAULTS_FILE: Final[Path] = CONFIG_DIR / DEFAULTS_FILE_NAME
DOMAINS_FILE: Final[Path] = CONFIG_DIR / DOMAINS_FILE_NAME
PORTS_FILE: Final[Path] = CONFIG_DIR / PORTS_FILE_NAME
PROJECTS_FILE: Final[Path] = CONFIG_DIR / PROJECTS_FILE_NAME
