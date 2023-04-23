from click import group, option, BOOL, STRING, INT

from . import handlers


@group('ports')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    handlers.init(rewrite)


@cli.command('allocate')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, prompt='Тип выделяемого порта')
@option('-c', '--count', type=INT, default=1, required=False)
def allocate(project: str, type: str, count: int):
    handlers.allocate(project, type, count)


@cli.command('free')
@option('--project', type=STRING, prompt='Имя проекта')
@option('-t', '--type', type=STRING, required=False)
@option('--port-index', type=INT, required=False)
def free(project: str, type: str | None, port_index: int | None):
    handlers.free(project, type, port_index)


@cli.command('ls')
@option('--project', type=STRING)
@option('-t', '--type', type=STRING, required=False)
def ls(project: str, type: str):
    handlers.show_project_ports(project, type)


@cli.command('status')
def status():
    handlers.show_server_ports()
