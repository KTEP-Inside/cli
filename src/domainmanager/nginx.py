import pathlib
import typing


SITES_AVAILABLE_DIRECTORY = pathlib.Path('/etc/nginx/sites-available')

SITES_ENABLE_DIRECTORY = pathlib.Path('/etc/nginx/sites-enable')

TEMPLATE_FILE = pathlib.Path(__file__).parent / 'template.conf'

DEFAULT_DOMAIN = 'ktep-inside.local'

LOGS_DIRECTORY = pathlib.Path('/web/sites/kinside')


class Site(typing.NamedTuple):
	subdomain: str
	domain: str
	active: bool


def create_nginx_config(
	subdomain: str,
	domain: str,
) -> None:
	path = SITES_AVAILABLE_DIRECTORY / f'{subdomain}.{domain}.conf'
	content = TEMPLATE_FILE.read_text().format(
		subdomain=subdomain,
		domain=domain
	)

	path.touch(exist_ok=True)
	path.write_text(content)


def create_nginx_logs_directory(
	subdomain: str,
	domain: str,
) -> None:
	path = LOGS_DIRECTORY / f'{subdomain}.{domain}' / 'logs'
	path.mkdir(parents=True, exist_ok=True)


def list_all_domains() -> None:
	sites = _get_available_sites()
	_print_sites(sites)


def _get_available_sites() -> list[Site]:
	sites: list[Site] = []
	for entity in SITES_AVAILABLE_DIRECTORY.iterdir():
		subdomain, domain = entity.stem.split('.', 1)
		activated = _is_site_activated(entity)
		sites.append(Site(subdomain, domain, activated))
	return sites


def _is_site_activated(config: pathlib.Path) -> bool:
	file = SITES_ENABLE_DIRECTORY / config.name
	return file.exists()


def _print_sites(sites: list[Site]) -> None:
	if len(sites) < 1:
		return None

	print('{:<15} {:<20} {}'. format('SUBDOMAIN', 'DOMAIN', 'STATUS'))
	for site in sites:
		status = 'active' if site.active else 'inactive'
		print(f'{site.subdomain:<15} {site.domain:<20} {status}')


def list_active_domains() -> None:
	sites = [site for site in _get_available_sites() if site.active]
	_print_sites(sites)


def list_inactive_domains() -> None:
	sites = [site for site in _get_available_sites() if not site.active]
	_print_sites(sites)
