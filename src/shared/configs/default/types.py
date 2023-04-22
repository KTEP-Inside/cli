from typing import TypedDict, Dict

from ..base_config_file import BaseConfigFile

from .config import DEFAULT_CONFIG


class DomainInfo(TypedDict):
    domain: str
    certDir: str
    nginxConfigDir: str
    enabledNginxConfigDir: str


class PortInfo(TypedDict):
    min: int
    max: int


class DefaultConfig(TypedDict):
    domain: DomainInfo
    ports: Dict[str, PortInfo]


class DefaultConfigFile(BaseConfigFile[DefaultConfig]):
    def __init__(self, path: str | None = None):
        _path = path or DEFAULT_CONFIG
        super().__init__(path=_path)
