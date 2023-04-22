from typing import TypedDict, Dict, List

from ..base_config_file import BaseConfigFile

from .config import DOMAINS_CONFIG


class DomainProjectInfo(TypedDict):
    enabled: bool
    fullDomain: str
    domain: str
    subdomain: str | None
    cert: str
    config: str


class DomainUsingInfo(TypedDict):
    list: List[str]
    map: Dict[str, str]


class DomainsConfig(TypedDict):
    using: DomainUsingInfo
    projects: Dict[str, DomainProjectInfo]


class DomainsConfigFile(BaseConfigFile[DomainsConfig]):
    def __init__(self, path: str | None = None):
        _path = path or DOMAINS_CONFIG
        super().__init__(path=_path)
