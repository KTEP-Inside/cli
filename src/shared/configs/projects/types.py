from typing import TypedDict, Dict, List, Union
from os.path import join

from ..base_config_file import BaseJSONConfigFile

from .config import PROJECTS_CONFIG, PROJECT_CONFIG_NAME


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


class ProjectDomainInfo(TypedDict):
    enabled: bool
    inject: bool | None
    fullDomain: str
    cert: str


class _ProjectPortsInfo(TypedDict):
    inject: bool | None


ProjectPortsInfo = Union[_ProjectPortsInfo, Dict[str, List[int]]]


class ProjectNetworkInfo(TypedDict):
    domain: ProjectDomainInfo
    ports: ProjectPortsInfo


class ProjectConfig(TypedDict):
    name: str
    envFile: str | None
    network: ProjectNetworkInfo


class ProjectConfigFile(BaseJSONConfigFile[ProjectConfig]):
    def __init__(self, name: str | None, path: str | None = None):
        projects = ProjectsConfigFile()
        _path = None

        if path:
            _path = path
        else:
            _path = join(projects.get_project(name)[
                         'dir'], PROJECT_CONFIG_NAME)

        super().__init__(_path)
