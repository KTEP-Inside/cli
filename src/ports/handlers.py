from click import echo
from json import dumps

from shared.lib import get_or_create
from shared.config import TEMPLATE_DIR
from shared.configs.default import DefaultConfigFile
from shared.configs.projects import \
    ProjectsConfigFile, ProjectConfigFile
from shared.configs.ports import  \
    PortsConfigFile, PORTS_CONFIG, \
    PORTS_CONFIG_NAME, PortsUsingPortInfo

from .lib import  \
    validate_port_type, allocate_ports, \
    has_ports, free_ports_by_type


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


def allocate(project_name: str, port_type: str, count: int):
    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile()

    default_config = default_config_file.config
    ports_config = ports_config_file.config

    validate_port_type(default_config, port_type)

    using_port_info = ports_config['using'][port_type]
    ports = allocate_ports(
        using_port_info=using_port_info,
        max=default_config['ports'][port_type]['max'],
        count=count)

    projects = ports_config['projects']
    ports_project = get_or_create(projects, project_name, {})
    ports_project_type = get_or_create(ports_project, port_type, [])
    ports_project_type += ports

    ports_config_file.save()

    sync_project_config(project_name)
    sync_projects_config(project_name)


def free(project_name: str, port_type: str | None, port_index: int | None):
    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile()

    default_config = default_config_file.config

    if port_index != None:
        validate_port_type(default_config, port_type)

    ports_config = ports_config_file.config

    using = ports_config['using']
    projects = ports_config['projects']
    project = ports_config_file.get_by_project_or_raise(project_name)

    deleting_types = []
    if port_type:
        deleting_types.append(port_type)
    else:
        deleting_types = project.keys()

    for port_type in deleting_types:
        free_ports_by_type(type=port_type, index=port_index,
                           project=project,
                           using=using)

    if not has_ports(project):
        projects.pop(project_name)

    ports_config_file.save()

    sync_project_config(project_name)
    sync_projects_config(project_name)


def show_project_ports(project_name: str, port_type: str):
    default_config_file = DefaultConfigFile()
    ports_config_file = PortsConfigFile()

    if port_type:
        validate_port_type(default_config_file.config, port_type)

    project_ports_config = ports_config_file.get_by_project_or_raise(
        project_name)

    show = project_ports_config.get(
        port_type) if port_type else project_ports_config

    if not show or not len(show):
        echo(f'Такого типа порты не выделены для проекта {project_name}')
        return

    echo(dumps(show, indent=2))


def show_server_ports():
    ports_config_file = PortsConfigFile()
    echo(dumps(ports_config_file.config['using'], indent=2))


def sync_project_config(project_name: str) -> None:
    project_config_file = ProjectConfigFile(project_name)
    ports_config_file = PortsConfigFile()

    project_config = project_config_file.config
    ports_config = ports_config_file.config

    project_ports = ports_config['projects'].get(project_name, {})

    for port_type in project_ports:
        project_config['network']['ports'][port_type] = project_ports[port_type]

    project_config_file.save()


def sync_projects_config(project_name: str) -> None:
    ports_config_file = PortsConfigFile()
    projects_config_file = ProjectsConfigFile()

    projects = ports_config_file.config['projects']
    use_ports = False

    if not has_ports(projects.get(project_name, {})):
        use_ports = False
    else:
        use_ports = True

    projects_config_file.get_project(project_name)['use_ports'] = use_ports
    projects_config_file.save()
