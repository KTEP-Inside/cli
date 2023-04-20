from typing import TypedDict, Dict


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
