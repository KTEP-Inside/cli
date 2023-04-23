from click import echo
from click.exceptions import FileError
from shutil import copyfile
from os import getcwd
from os.path import join
from pathlib import Path

from ports import ports_handlers
from shared.config import TEMPLATE_DIR, DEFAULT_ENV_FILE_NAME
from shared.configs.env import EnvConfigFile
from shared.configs.projects import \
    ProjectInfo, ProjectsConfigFile, \
    PROJECTS_CONFIG, PROJECTS_CONFIG_NAME, \
    ProjectConfigFile, PROJECT_CONFIG_NAME

from .lib import filter_injected_keys


def init(rewrite: bool):
    if not rewrite and PROJECTS_CONFIG.exists():
        return

    copyfile(TEMPLATE_DIR / PROJECTS_CONFIG_NAME,  PROJECTS_CONFIG)


def create(project_name: str):
    current_dir = getcwd()
    current_dir_config = Path(join(current_dir, PROJECT_CONFIG_NAME))

    if current_dir_config.exists():
        project_config_file = ProjectConfigFile(
            path=current_dir_config, name=None)
        name = project_config_file.config['name']
        echo(
            f'В данной директории уже существует проект с именем {name}')
        return

    _create_project_config(project_name, current_dir, )

    project: ProjectInfo = {
        'dir': current_dir,
        'use_ports': False,
        'use_domains': False
    }
    projects_config_file = ProjectsConfigFile()
    projects_config_file.config[project_name] = project
    projects_config_file.save()


def sync(project_name: str):
    projects_config_file = ProjectsConfigFile()
    project = projects_config_file.get_project_or_raise(project_name)

    _create_project_config(project_name, project['dir'])

    if project['use_ports']:
        ports_handlers.sync_project_config(project_name)
        pass

    if project['use_domains']:
        pass


def update(project_name: str):
    echo(f'Проект {project_name}')
    echo('WORK IN PROGRESS')
    pass


def remove(project_name: str):
    projects_config_file = ProjectsConfigFile()
    project_config_file = ProjectConfigFile(project_name)
    project = projects_config_file.get_project_or_raise(project_name)

    if project['use_ports']:
        ports_handlers.free(project_name, None, None)

    if project['use_domains']:
        pass

    projects_config_file.config.pop(project_name)
    projects_config_file.save()
    project_config_file.remove()


def show_all_projects():
    projects_config_file = ProjectsConfigFile()
    projects_config = projects_config_file.config

    template = "{name:<15} {dir:<25}"

    echo(template.format(name='NAME', dir='DIRECTORY'))
    for name in projects_config:
        dir = projects_config[name]['dir']

        echo(template.format(name=name, dir=dir))


def inject_env_variables(project_name: str):
    projects_config_file = ProjectsConfigFile()
    project = projects_config_file.get_project_or_raise(project_name)
    project_config_file = ProjectConfigFile(project_name)
    project_config = project_config_file.config

    env_file_name = project_config['envFile'] or DEFAULT_ENV_FILE_NAME
    env_file_path = Path(join(project['dir'], env_file_name))

    if not env_file_path.exists():
        env_file_path.touch()

    env_file = EnvConfigFile(env_file_path)

    network = project_config['network']
    if network['ports']['inject']:
        filtered_ports = dict(
            filter(filter_injected_keys, network['ports'].items()))
        env_file.update(filtered_ports)
    if network['domain']['inject']:
        filtered_domain = dict(
            filter(filter_injected_keys, network['domain'].items()))
        env_file.update(filtered_domain)

    env_file.save()


def _create_project_config(project_name: str, dir: str) -> ProjectConfigFile:
    if not PROJECTS_CONFIG.exists():
        echo('Глобальный файл проектов не найден. Пожалуйста, пересоздайте все глобальные файлы командой kinsidectl config init --rewrite', err=True)
        raise FileError('Нет глобального файла конфигурации')

    template_config_file = ProjectConfigFile(
        None, path=TEMPLATE_DIR / PROJECT_CONFIG_NAME)
    template_config_file.config['name'] = project_name

    template_config_file.save(Path(join(dir, PROJECT_CONFIG_NAME)))

    return template_config_file
