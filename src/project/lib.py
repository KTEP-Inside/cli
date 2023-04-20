from pathlib import Path
from typing import Dict

from config import read_config

def get_project(projects_file: Path, name: str) -> Dict | None:
    return read_config(projects_file).get(name)