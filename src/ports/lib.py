from typing import List

from shared.lib import read_config, write_config

from .config import PORTS_CONFIG
from .types import PortsConfig, PortsUsingPortInfo


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
