from click import group, option, echo, BOOL, STRING, INT
from json import dumps

from shared.lib import get_or_create
from shared.config import TEMPLATE_DIR
from shared.configs.ports import PORTS_CONFIG, PortsConfigFile, \
    PORTS_CONFIG_NAME,  PortsUsingPortInfo
from shared.configs.projects import ProjectConfigFile, ProjectsConfigFile
from shared.configs.default import DefaultConfigFile

from .lib import allocate_ports, has_ports, raise_invalid_port_type, free_ports_by_type


@group('ports')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    if not rewrite and PORTS_CONFIG.exists():
        return

    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile(path=TEMPLATE_DIR / PORTS_CONFIG_NAME)

    ports_config = ports_config_file.config
    ports_info = default_config_file.config['ports']

    for port_type in ports_info:
        info: PortsUsingPortInfo = {
            'next': ports_info[port_type]['min'],
            'free': []
        }

        ports_config['using'][port_type] = info

    ports_config_file.save(PORTS_CONFIG)


@cli.command('create')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, prompt='Тип выделяемого порта')
@option('-c', '--count', type=INT, default=1, required=False)
def create(project: str, type: str, count: int):
    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile()
    projects_config_file = ProjectsConfigFile()
    project_config_file = ProjectConfigFile(project)

    default_config = default_config_file.config
    project_config = project_config_file.config
    ports_config = ports_config_file.config

    raise_invalid_port_type(default_config, type)

    using_port_info = ports_config['using'][type]
    ports = allocate_ports(
        using_port_info=using_port_info,
        max=default_config['ports'][type]['max'],
        count=count)

    project_ports = get_or_create(project_config['network']['ports'], type, [])
    project_ports += ports

    projects = ports_config['projects']
    ports_project = get_or_create(projects, project, {})
    ports_project_type = get_or_create(ports_project, type, [])
    ports_project_type += ports

    projects_config_file.get_project(project)['usePorts'] = True

    ports_config_file.save()
    projects_config_file.save()
    project_config_file.save()


@cli.command('remove')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, required=False)
@option('--port-index', type=INT, required=False)
def remove(project: str, type: str | None, port_index: int | None):
    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile()
    projects_config_file = ProjectsConfigFile()
    project_config_file = ProjectConfigFile(project)

    default_config = default_config_file.config

    raise_invalid_port_type(default_config, type)

    project_config = project_config_file.config
    ports_config = ports_config_file.config

    using = ports_config['using']
    projects = ports_config['projects']
    if type:
        free_ports_by_type(type=type, index=port_index,
                           network=project_config['network'], project=projects[project],
                           using=ports_config['using'])
    else:
        for type in using.keys():
            if not project_config['network']['ports'].get(type):
                continue

            free_ports_by_type(type=type, index=port_index,
                               network=project_config['network'], project=projects[project],
                               using=ports_config['using'])

    if not has_ports(projects[project]):
        projects.pop(project)
        projects_config_file.get_project(project)['usePorts'] = False

    ports_config_file.save()
    projects_config_file.save()
    project_config_file.save()


@cli.command('ls')
@option('--project', type=STRING)
@option('-t', '--type', type=STRING, required=False)
def ls(project: str, type: str):
    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile()

    raise_invalid_port_type(default_config_file.config, type)

    ports_config = ports_config_file.config

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
    ports_config_file = PortsConfigFile()
    echo(dumps(ports_config_file.config, indent=2))
