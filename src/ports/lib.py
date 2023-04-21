from typing import List
from functools import reduce

from project import ProjectConfig
from shared.lib import read_config, write_config

from .config import PORTS_CONFIG
from .types import PortsConfig, PortsUsingPortInfo, PortsProjectInfo


def read_ports_config() -> PortsConfig:
    return read_config(PORTS_CONFIG)


def write_ports_config(config: PortsConfig) -> None:
    write_config(PORTS_CONFIG, config)


def allocate_ports(using_port_info: PortsUsingPortInfo, max: int, count: int = 1) -> List[int]:
    ports = []
    if len(using_port_info['free']) > 0:
        if len(using_port_info['free']) >= count:
            ports = using_port_info['free'][0:count]
            using_port_info['free'] = using_port_info['free'][count:]
            count = 0
        else:
            ports = using_port_info['free']
            using_port_info['free'] = []
            count -= len(ports)

    for port in range(using_port_info['next'], max + 1):
        if not count:
            using_port_info['next'] = port
            break
        ports.append(port)
        count -= 1

    return ports


def free_ports(type: str,
               ports_config: PortsConfig,
               project_config: ProjectConfig,
               index: int | None = None) -> None:
    network = project_config['network']
    free_ports_by_type(
        type=type, using=ports_config['using'][type], ports_project_config=network['ports'], index=index)
    ports_config['projects'][project_config['name']][type] = network['ports'][type]


def free_ports_by_type(type: str, using: PortsUsingPortInfo,
                       ports_project_config: PortsProjectInfo,
                       index: int | None = None) -> None:
    free = ports_project_config[type][index: index +
                                      1] if index != None else list(ports_project_config[type])
    for port in free:
        ports_project_config[type].remove(port)
    
    
    using['free'] += free


def has_ports(ports_project_info: PortsProjectInfo) -> bool:
    return reduce(lambda reduced, ports: reduced and len(ports), ports_project_info.values(), True)
