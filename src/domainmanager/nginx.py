import pathlib


TEMPLATE_FILE = pathlib.Path(__file__).parent / 'template.conf'

SITES_AVAILABLE_DIRECTORY = pathlib.Path('/etc/nginx/sites-available')

CONFIG_NAME_TEMPLATE = '{subdomain}.{domain}.conf'

LOGS_DIRECTORY = pathlib.Path('/web/sites/kinside')


def create_nginx_config(
	subdomain: str,
	domain: str,
) -> None:
	path = _resolve_config_path(subdomain, domain)
	content = _generate_config_from_template(subdomain, domain)
	_write_config(path, content)


def _resolve_config_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	name = CONFIG_NAME_TEMPLATE.format(subdomain=subdomain, domain=domain)
	return SITES_AVAILABLE_DIRECTORY / name


def _generate_config_from_template(
	subdomain: str,
	domain: str,
) -> str:
	content = TEMPLATE_FILE.read_text()
	return content.format(subdomain=subdomain, domain=domain)

def _write_config(path: pathlib.Path, content: str) -> None:
	path.touch(exist_ok=True)
	path.write_text(content)


def create_nginx_logs_directory(
	subdomain: str,
	domain: str,
) -> None:
	path = LOGS_DIRECTORY / f'{subdomain}.{domain}' / 'logs'
	path.mkdir(parents=True, exist_ok=True)
