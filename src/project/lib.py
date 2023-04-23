from typing import Tuple, Any
from click.exceptions import BadArgumentUsage

from shared.configs.projects import \
    ProjectsConfigFile, ProjectInfo

from .config import INJECT_BLACKLIST


def get_project_or_raise(projects_config_file: ProjectsConfigFile, project_name: str) -> ProjectInfo:
    project = projects_config_file.get_project(project_name)

    if not project:
        raise BadArgumentUsage(
            f'Проекта с именем {project_name} не существует')

    return project


def filter_injected_keys(pair: Tuple[str, Any]) -> bool:
    return pair[0] not in INJECT_BLACKLIST
