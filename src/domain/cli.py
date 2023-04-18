import click

from .certificates import create_ssl_certificate
from .nginx import list_inactive_domains, \
    DEFAULT_DOMAIN, \
    create_nginx_config, \
    create_nginx_logs_directory,  \
    list_active_domains,  \
    list_all_domains
from .sources import create_sources_directory


@click.group("domain")
def cli() -> None:
    pass


@cli.command('new')
@click.argument('subdomain')
@click.argument('domain', required=False, default=DEFAULT_DOMAIN)
@click.option('--no-source-dir', is_flag=True, default=False)
@click.option('--activate', is_flag=True, default=False)
def new_domain(
        subdomain: str,
        domain: str,
        no_source_dir: bool,
        activate: bool,
) -> None:
    create_nginx_config(subdomain, domain)
    create_nginx_logs_directory(subdomain, domain)
    create_ssl_certificate(subdomain, domain)
    if not no_source_dir:
        create_sources_directory(subdomain)


@cli.command('list')
@click.option('--active', is_flag=True, default=False)
@click.option('--inactive', is_flag=True, default=False)
def list_domains(
        active: bool,
        inactive: bool,
) -> None:
    if active:
        list_active_domains()
    elif inactive:
        list_inactive_domains()
    else:
        list_all_domains()


def run() -> None:
    cli(prog_name='kinsidectl domain')
