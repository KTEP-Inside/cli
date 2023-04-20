from typing import TypedDict, Dict, List, Union

class ProjectInfo(TypedDict):
    dir: str
    usePorts: bool
    useDomain: bool


ProjectsConfig = Dict[str, ProjectInfo]


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
