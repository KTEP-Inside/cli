from click import option, group, BOOL, STRING
from typing import Any

from . import handlers


@group('config')
def cli():
    pass


@cli.command('init')
@option('--rewrite', is_flag=True, default=False, type=BOOL)
def init(rewrite: bool):
    handlers.init(rewrite)


@cli.command('get')
@option('--key', type=STRING, required=False)
def get(key: str | None):
    handlers.get(key)


@cli.command('set')
@option('--key', type=STRING)
@option('--value')
def set(key: str, value: Any):
    handlers.set(key, value)
