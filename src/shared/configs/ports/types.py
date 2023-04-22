from typing import TypedDict, Dict, List

from ..base_config_file import BaseConfigFile

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


class PortsConfigFile(BaseConfigFile[PortsConfig]):

    def __init__(self, path: str | None = None):
        _path = path or PORTS_CONFIG
        super().__init__(path=_path)

    def get_by_project(self, project_name: str):
        return self.config['projects'].get(project_name)
