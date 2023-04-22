from click import group, option, STRING, argument, echo, BOOL
from os import getcwd
from os.path import join
from pathlib import Path
from shutil import copyfile

from shared.config import TEMPLATE_DIR
from shared.configs.projects import ProjectConfigFile, ProjectsConfigFile, \
    PROJECTS_CONFIG_NAME, PROJECTS_CONFIG, \
    ProjectInfo, PROJECT_CONFIG_NAME


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
        project_config_file = ProjectConfigFile(
            path=current_dir_config, name=None)
        name = project_config_file.config['name']
        echo(
            f'В данной директории уже существует проект с именем {name}')
        return

    template_config_file = ProjectConfigFile(
        None, path=TEMPLATE_DIR / PROJECT_CONFIG_NAME)
    template_config_file.config['name'] = project_name

    template_config_file.save(current_dir_config)

    if not PROJECTS_CONFIG.exists():
        echo('Глобальный файл проектов не найден. Пожалуйста, пресоздайте все глобальные файлы командой kinsidectl config init --rewrite')
        return

    project: ProjectInfo = {
        'dir': current_dir,
        'useDomain': False,
        'usePorts': False
    }

    projects_config_file = ProjectsConfigFile()
    projects_config_file.config[project_name] = project
    projects_config_file.save()


@cli.command('recreate')
@argument('project-name', type=STRING)
def recreate(project_name: str):
    projects_config_file = ProjectsConfigFile()
    project = projects_config_file.get_project(project_name)

    if not project:
        echo(f'Проекта с именем {project_name} не существует')
        return

    project_config_file = ProjectConfigFile(
        None, path=TEMPLATE_DIR / PROJECT_CONFIG_NAME)

    project_config_file.config['name'] = project_name

    if project['usePorts']:

        pass

    if project['useDomain']:
        pass

    project_config_path = Path(join(project['dir'], PROJECT_CONFIG_NAME))
    project_config_file.save(path=project_config_path)


@cli.command('sync')
def sync():
    echo('WORK IN PROGRESS')
    pass


@cli.command('remove')
@argument('project-name', type=STRING)
def remove(project_name: str):
    projects_config_file = ProjectsConfigFile()
    project_config_file = ProjectConfigFile(project_name)
    project = projects_config_file.get_project(project_name)

    if project['usePorts']:
        # remove_ports(project=project_config['name'])
        pass

    if project['useDomain']:
        pass

    projects_config_file.config.pop(project_name)
    projects_config_file.save()
    project_config_file.remove()


@cli.command('ls')
def ls():
    projects_config_file = ProjectsConfigFile()
    projects_config_config = projects_config_file.config

    template = "{name:<15} {dir:<25}"

    echo(template.format(name='NAME', dir='DIRECTORY'))
    for name in projects_config_config:
        dir = projects_config_config[name]['dir']

        echo(template.format(name=name, dir=dir))


@cli.command('inject')
@argument('project-name', type=STRING)
def inject(project_name: str):
    pass
