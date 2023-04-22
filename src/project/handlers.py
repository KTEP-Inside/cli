from click import echo
from click.exceptions import FileError
from shutil import copyfile
from os import getcwd
from os.path import join
from pathlib import Path

from ports import ports_handlers
from shared.config import TEMPLATE_DIR
from shared.configs.projects import \
    ProjectInfo, ProjectsConfigFile, \
    PROJECTS_CONFIG, PROJECTS_CONFIG_NAME, \
    ProjectConfigFile, PROJECT_CONFIG_NAME

from .lib import get_project_or_raise


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
    project = get_project_or_raise(projects_config_file, project_name)

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
    project = get_project_or_raise(projects_config_file, project_name)

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
    echo(f'Проект {project_name}')
    echo('WORK IN PROGRESS')
    pass


def _create_project_config(project_name: str, dir: str) -> ProjectConfigFile:
    if not PROJECTS_CONFIG.exists():
        echo('Глобальный файл проектов не найден. Пожалуйста, пересоздайте все глобальные файлы командой kinsidectl config init --rewrite', err=True)
        raise FileError('Нет глобального файла конфигурации')

    template_config_file = ProjectConfigFile(
        None, path=TEMPLATE_DIR / PROJECT_CONFIG_NAME)
    template_config_file.config['name'] = project_name

    template_config_file.save(Path(join(dir, PROJECT_CONFIG_NAME)))

    return template_config_file
