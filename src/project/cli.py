from click import group, option, STRING, argument, BOOL
from . import handlers


@group('project')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    return handlers.init(rewrite)


@cli.command('create')
@argument('project-name', type=STRING)
def create(project_name: str):
    handlers.create(project_name)


@cli.command('sync')
@argument('project-name', type=STRING)
def update(project_name: str):
    handlers.sync(project_name)


@cli.command('update')
@argument('project-name', type=STRING)
def update(project_name: str):
    handlers.update(project_name)


@cli.command('remove')
@argument('project-name', type=STRING)
def remove(project_name: str):
    handlers.remove(project_name)


@cli.command('ls')
def ls():
    handlers.show_all_projects()


@cli.command('inject')
@argument('project-name', type=STRING)
def inject(project_name: str):
    handlers.inject_env_variables(project_name)
