from click import group, option, echo, BOOL, STRING, INT
from click.exceptions import BadOptionUsage
from pathlib import Path
from json import dumps

from shared.lib import read_config
from shared.config import TEMPLATE_DIR
from config import read_default_config
from project import read_projects_config, read_project_config, write_project_config, write_projects_config, PROJECT_CONFIG_NAME

from .config import PORTS_CONFIG, PORTS_CONFIG_NAME
from .lib import read_ports_config, allocate_ports, write_ports_config, has_ports, free_ports
from .types import PortsConfig, PortsUsingPortInfo


@group('ports')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    if not rewrite and PORTS_CONFIG.exists():
        return

    default_config = read_default_config()
    ports_config: PortsConfig = read_config(TEMPLATE_DIR / PORTS_CONFIG_NAME)
    ports_info = default_config['ports']

    for port_type in ports_info:
        info: PortsUsingPortInfo = {
            'next': ports_info[port_type]['min'],
            'free': []
        }

        ports_config['using'][port_type] = info

    write_ports_config(ports_config)


@cli.command('create')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, prompt='Тип выделяемого порта')
@option('-c', '--count', type=INT, default=1, required=False)
def create(project: str, type: str, count: int):
    default_config = read_default_config()
    ports_config = read_ports_config()
    projects_config = read_projects_config()

    project_config_path = Path(
        projects_config[project]['dir']) / PROJECT_CONFIG_NAME
    project_config = read_project_config(project_config_path)

    ports_info = default_config['ports']
    port_info = ports_info.get(type)

    if not port_info:
        echo('Такого типа портов не существует')
        types = ', '.join([type for type in ports_info])
        echo(f'Доступны следующие типы портов {types}')
        raise BadOptionUsage(
            option_name='-t', message='Неправильный тип порта')

    using_port_info = ports_config['using'][type]
    ports = allocate_ports(
        using_port_info, default_config['ports'][type]['max'], count)

    project_config['network']['ports'][type] = ports

    ports_project = ports_config['projects'].get(project)
    if not ports_project:
        ports_config['projects'][project] = {}
        ports_project = ports_config['projects'].get(project)

    ports_project[type] = ports

    projects_config[project]['usePorts'] = True

    write_projects_config(projects_config)
    write_project_config(project_config_path, project_config)
    write_ports_config(ports_config)


@cli.command('remove')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, required=False)
@option('--port-index', type=INT, required=False)
def remove(project: str, type: str | None, port_index: int | None):
    ports_config = read_ports_config()
    projects_config = read_projects_config()
    project_config_path = Path(
        projects_config[project]['dir']) / PROJECT_CONFIG_NAME
    project_config = read_project_config(project_config_path)

    using = ports_config['using']

    if type:
        free_ports(ports_config=ports_config, type=type,
                   project_config=project_config, index=port_index)
    else:
        for type in using.keys():
            if not project_config['network']['ports'].get(type):
                continue
            free_ports(ports_config=ports_config, type=type,
                       project_config=project_config, index=port_index)

    if not has_ports(ports_config['projects'].get(project)):
        ports_config['projects'].pop(project)
        projects_config.get(project)['usePorts'] = False

    write_projects_config(projects_config)
    write_project_config(project_config_path, project_config)
    write_ports_config(ports_config)


@cli.command('ls')
@option('--project', type=STRING)
@option('-t', '--type', type=STRING, required=False)
def ls(project: str, type: str):
    ports_config = read_ports_config()

    project_ports_config = ports_config['projects'].get(project)
    if not project_ports_config:
        echo('Для такого проекта не выделен ни один порт')
        return

    show = project_ports_config.get(type) if type else project_ports_config

    if not show or len(show):
        echo('Такого типа порты не выделены ')
        return

    echo(dumps(show, indent=2))


@cli.command('status')
def status():
    ports_config = read_ports_config()
    echo(dumps(ports_config, indent=2))
