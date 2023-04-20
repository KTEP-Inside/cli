from click import group, option, STRING, argument, echo, BOOL
from os import getcwd, remove as rm
from os.path import join
from pathlib import Path
from shutil import copyfile

from config import PROJECTS_FILE, read_config, TEMPLATE_DIR, PROJECT_FILE_NAME, write_config, PROJECTS_FILE_NAME

from .lib import get_project

@group('project')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    if rewrite or not PROJECTS_FILE.exists():
        copyfile(TEMPLATE_DIR / PROJECTS_FILE_NAME,  PROJECTS_FILE)


@cli.command('create')
@argument('project-name', type=STRING)
def create(project_name: str):
    current_dir = getcwd()

    current_dir_config = Path(join(current_dir, PROJECT_FILE_NAME))

    if current_dir_config.exists():
        config = read_config(current_dir_config)
        name = config['name']
        echo(
            f'В данной директории уже существует проект с именем {name}')
        return

    template_config = read_config(TEMPLATE_DIR / PROJECT_FILE_NAME)
    template_config['name'] = project_name

    write_config(current_dir_config, template_config)

    if not PROJECTS_FILE.exists():
        echo('Глобальный файл проектов не найден. Пожалуйста, пресоздайте все глобальные файлы командой kinsidectl config init --rewrite')
        return

    project = dict(
        [["dir", current_dir], ["usePorts", False], ["useDomain", False]])

    projects_config = read_config(PROJECTS_FILE)
    projects_config[project_name] = project

    write_config(PROJECTS_FILE, projects_config)


@cli.command('recreate')
@argument('project-name', type=STRING)
def recreate(project_name: str):
    project = get_project(PROJECTS_FILE, project_name)

    if not project:
        echo(f'Проекта с именем {project_name} не существует')
        return

    new_project_config = read_config(TEMPLATE_DIR / PROJECT_FILE_NAME)

    new_project_config['name'] = project_name

    if project['usePorts']:
        pass

    if project['useDomain']:
        pass

    new_project_config_path = Path(join(project['dir'], PROJECT_FILE_NAME))

    write_config(new_project_config_path, new_project_config)


@cli.command('sync')
def sync():
    echo('WORK IN PROGRESS')
    pass


@cli.command('remove')
@argument('project-name', type=STRING)
def remove(project_name: str):
    projects = read_config(PROJECTS_FILE)
    project = projects.get(project_name)

    rm(join(project['dir'], PROJECT_FILE_NAME))
    
    if project['usePorts']:
        pass
    
    if project['useDomain']:
        pass
    
    projects.pop(project_name)
    
    write_config(PROJECTS_FILE, projects)
    


@cli.command('ls')
def ls():
    projects = read_config(PROJECTS_FILE)

    template = "{name:<15} {dir:<25}"

    echo(template.format(name='NAME', dir='DIRECTORY'))
    for name in projects:
        dir = projects[name]['dir']

        echo(template.format(name=name, dir=dir))


@cli.command('inject')
@argument('project-name', type=STRING)
def inject(project_name: str):
    pass
