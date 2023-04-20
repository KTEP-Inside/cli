from pathlib import Path

from shared.lib import read_config, write_config

from .config import PROJECTS_CONFIG
from .types import ProjectConfig, ProjectsConfig


def read_project_config(path: Path) -> ProjectConfig:
    return read_config(path)


def write_project_config(path: Path, config: ProjectConfig) -> None:
    write_config(path, config)


def read_projects_config() -> ProjectsConfig:
    return read_config(PROJECTS_CONFIG)


def write_projects_config(config: ProjectsConfig) -> None:
    write_config(PROJECTS_CONFIG, config)
