from click.exceptions import BadOptionUsage
from typing import TypedDict, Dict, List

from ..base_config_file import BaseJSONConfigFile

from .config import PORTS_CONFIG


class PortsUsingPortInfo(TypedDict):
    next: int
    free: List[int]


PortsUsingInfo = Dict[str, PortsUsingPortInfo]
PortsProjectInfo = Dict[str, List[int]]
PortsProjectsInfo = Dict[str, PortsProjectInfo]


class PortsConfig(TypedDict):
    using: PortsUsingInfo
    projects: PortsProjectsInfo


class PortsConfigFile(BaseJSONConfigFile[PortsConfig]):

    def __init__(self, path: str | None = None):
        _path = path or PORTS_CONFIG
        super().__init__(path=_path)

    def get_by_project(self, project_name: str) -> PortsProjectInfo | None:
        return self.config['projects'].get(project_name)

    def get_by_project_or_raise(self, project_name: str) -> PortsProjectInfo:
        project_ports = self.get_by_project(project_name)

        if not project_ports:
            raise BadOptionUsage(
                f'Для проекта {project_name} не выделен но один порт')

        return project_ports
