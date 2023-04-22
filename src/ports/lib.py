from typing import List
from click import echo
from click.exceptions import BadOptionUsage

from shared.configs.ports import PortsUsingPortInfo, PortsProjectInfo
from shared.configs.default import DefaultConfig
from shared.configs.projects import ProjectNetworkInfo


def allocate_ports(using_port_info: PortsUsingPortInfo, max: int, count: int = 1) -> List[int]:
    ports: List[int] = []

    if len(using_port_info['free']) > 0:
        ports = using_port_info['free'][0:count]
        using_port_info['free'] = using_port_info['free'][count:]
        count -= len(ports)

    for port in range(using_port_info['next'], max + 1):
        if count <= 0:
            using_port_info['next'] = port
            break

        ports.append(port)
        count -= 1

    return ports


def free_ports_by_type(type: str | None, using: PortsUsingPortInfo,
                       project: PortsProjectInfo,
                       network: ProjectNetworkInfo,
                       index: int | None = None) -> None:
    free = []
    print(project)

    if index != None:
        free = project[type][index: index + 1]
    else:
        free = list(project[type])

    for port in free:
        project[type].remove(port)

    using[type]['free'] += free

    network['ports'][type] = project[type]


def has_ports(ports_project_info: PortsProjectInfo) -> bool:
    for ports in ports_project_info.values():
        if len(ports) > 0:
            return True

    return False


def raise_invalid_port_type(default_config: DefaultConfig, type: str | None) -> None:
    if not type:
        return

    ports_info = default_config['ports']
    port_info = ports_info.get(type)

    if port_info:
        return

    echo('Такого типа портов не существует')
    types = ', '.join([type for type in ports_info])
    echo(f'Доступны следующие типы портов {types}')
    raise BadOptionUsage(
        option_name='-t', message='Неправильный тип порта')
