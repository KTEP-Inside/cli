from typing import TypedDict, Dict, List


class PortsUsingPortInfo(TypedDict):
    next: int
    free: List[int]

PortsUsingInfo = Dict[str, PortsUsingPortInfo]
PortsProjectInfo = Dict[str, List[int]]
PortsProjectsInfo = Dict[str, PortsProjectInfo]


class PortsConfig(TypedDict):
    using: PortsUsingInfo
    projects: PortsProjectsInfo
