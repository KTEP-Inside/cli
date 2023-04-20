from pathlib import Path

from shared.lib import read_config

from .config import PROJECTS_CONFIG
from .types import ProjectConfig, ProjectsConfig, ProjectInfo


def read_project_config(path: Path) -> ProjectConfig:
    return read_config(path)


def read_projects_config() -> ProjectsConfig:
    return read_config(PROJECTS_CONFIG)
