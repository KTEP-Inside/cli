from click import group, option, echo, BOOL, STRING, INT
from click.exceptions import BadOptionUsage
from pathlib import Path

from shared.lib import read_config
from shared.config import TEMPLATE_DIR
from config import read_default_config
from project import read_projects_config, read_project_config, write_project_config, write_projects_config, PROJECT_CONFIG_NAME

from .config import PORTS_CONFIG, PORTS_CONFIG_NAME
from .lib import read_ports_config, allocate_ports, write_ports_config
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
@option('--project', type=STRING)
@option('-t', '--type', type=STRING, required=False)
@option('--port-index', type=INT, default=0, required=False)
def remove(project: str, type: str, port_index: str):
    pass


@cli.command('ls')
@option('--project', type=STRING)
@option('-t', '--type', type=STRING, required=False)
def ls(project: str, type: str):
    pass


@cli.command('status')
def status():
    pass
