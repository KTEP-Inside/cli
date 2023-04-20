from click import group, option, STRING, argument, echo, BOOL
from os import getcwd, remove as rm
from os.path import join
from pathlib import Path
from shutil import copyfile

from shared.config import TEMPLATE_DIR
from shared.lib import write_config

from .types import ProjectInfo
from .config import PROJECTS_CONFIG, PROJECTS_CONFIG_NAME, PROJECT_CONFIG_NAME
from .lib import read_projects_config, read_project_config


@group('project')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    if rewrite or not PROJECTS_CONFIG.exists():
        copyfile(TEMPLATE_DIR / PROJECTS_CONFIG_NAME,  PROJECTS_CONFIG)


@cli.command('create')
@argument('project-name', type=STRING)
def create(project_name: str):
    current_dir = getcwd()

    current_dir_config = Path(join(current_dir, PROJECT_CONFIG_NAME))

    if current_dir_config.exists():
        config = read_project_config(current_dir_config)
        name = config['name']
        echo(
            f'В данной директории уже существует проект с именем {name}')
        return

    template_config = read_project_config(TEMPLATE_DIR / PROJECT_CONFIG_NAME)
    template_config['name'] = project_name

    write_config(current_dir_config, template_config)

    if not PROJECTS_CONFIG.exists():
        echo('Глобальный файл проектов не найден. Пожалуйста, пресоздайте все глобальные файлы командой kinsidectl config init --rewrite')
        return

    project: ProjectInfo = {
        'dir': current_dir,
        'useDomain': False,
        'usePorts': False
    }

    projects_config = read_projects_config()
    projects_config[project_name] = project

    write_config(PROJECTS_CONFIG, projects_config)


@cli.command('recreate')
@argument('project-name', type=STRING)
def recreate(project_name: str):
    projects = read_projects_config()
    project = projects.get(project_name)

    if not project:
        echo(f'Проекта с именем {project_name} не существует')
        return

    project_config = read_project_config(TEMPLATE_DIR / PROJECT_CONFIG_NAME)

    project_config['name'] = project_name

    if project['usePorts']:
        pass

    if project['useDomain']:
        pass

    project_config_path = Path(join(project['dir'], PROJECT_CONFIG_NAME))

    write_config(project_config_path, project_config)


@cli.command('sync')
def sync():
    echo('WORK IN PROGRESS')
    pass


@cli.command('remove')
@argument('project-name', type=STRING)
def remove(project_name: str):
    projects = read_projects_config()
    project = projects.get(project_name)

    rm(join(project['dir'], PROJECT_CONFIG_NAME))

    if project['usePorts']:
        pass

    if project['useDomain']:
        pass

    projects.pop(project_name)

    write_config(PROJECTS_CONFIG, projects)


@cli.command('ls')
def ls():
    projects = read_projects_config()

    template = "{name:<15} {dir:<25}"

    echo(template.format(name='NAME', dir='DIRECTORY'))
    for name in projects:
        dir = projects[name]['dir']

        echo(template.format(name=name, dir=dir))


@cli.command('inject')
@argument('project-name', type=STRING)
def inject(project_name: str):
    pass
