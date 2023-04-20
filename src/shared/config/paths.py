from typing import Final
from pathlib import Path
from os.path import join

TEMPLATE_DIR: Final[Path] = Path("templates").resolve()
CONFIG_DIR: Final[Path] = Path(join(Path.home(), '.kinsidectl'))
