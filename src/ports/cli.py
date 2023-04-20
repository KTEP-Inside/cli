from click import group, option, echo, BOOL, STRING, INT
from click.exceptions import BadOptionUsage

from shared.lib import write_config, read_config
from shared.config import TEMPLATE_DIR
from config import read_default_config
from project import read_projects_config

from .config import PORTS_CONFIG, PORTS_CONFIG_NAME
from .lib import read_ports_config
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
            'free': list()
        }

        ports_config['using'][port_type] = info

    write_config(PORTS_CONFIG, ports_config)


@cli.command('create')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, prompt='Тип выделяемого порта')
@option('-c', '--count', type=INT, default=1, required=False, prompt='Количество портов')
def create(project: str, port_type: str, count: int):
    default_config = read_default_config()
    ports_config = read_ports_config()
    projects_config = read_projects_config()
    
    ports_info = default_config['ports']
    
    if not (port_type in ports_info):
        echo('Такого типа портов не существует')
        types = [type for type in ports_info]
        echo(f'Дотупны следующие типы портов {types}')
        raise BadOptionUsage('')

    pass


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
