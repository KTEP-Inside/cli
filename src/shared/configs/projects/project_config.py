from typing import TypedDict, Dict, List, Union
from os.path import join

from ..base_config_file import BaseJSONConfigFile

from .projects_config import ProjectsConfigFile
from .config import PROJECT_CONFIG_NAME


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
            _path = join(projects.get_project_or_raise(name)[
                         'dir'], PROJECT_CONFIG_NAME)

        super().__init__(_path)
