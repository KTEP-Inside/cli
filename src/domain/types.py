from typing import TypedDict, Dict, List


class DomainProjectInfo(TypedDict):
    domain: str
    certDir: str
    nginxConfigDir: str
    enabledNginxConfigDir: str


DomainsUsingInfo = List[str]
DomainsUsingMapInfo = Dict[str, str]
DomainsProjectsInfo = Dict[str, DomainProjectInfo]


class DomainsConfig(TypedDict):
    using: DomainsUsingInfo
    map: DomainsUsingMapInfo
    projects: DomainsProjectsInfo
