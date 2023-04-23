from typing import TypedDict, Dict
from click.exceptions import BadArgumentUsage

from ..base_config_file import BaseJSONConfigFile

from .config import PROJECTS_CONFIG


class ProjectInfo(TypedDict):
    dir: str
    use_ports: bool
    use_domains: bool


ProjectsConfig = Dict[str, ProjectInfo]


class ProjectsConfigFile(BaseJSONConfigFile[ProjectsConfig]):
    def __init__(self, path: str | None = None):
        _path = path or PROJECTS_CONFIG
        super().__init__(path=_path)

    def get_project(self, name: str) -> ProjectInfo | None:
        return self.config.get(name)

    def get_project_or_raise(self, name: str) -> ProjectInfo:
        project = self.get_project(name)

        if not project:
            raise BadArgumentUsage(
                f'Проекта с именем {name} не существует')

        return project
