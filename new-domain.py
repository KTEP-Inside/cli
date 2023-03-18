#!/usr/bin/env python3
import argparse
import pathlib
import subprocess


DOCUMENTS_DIRECTORY_PATH = pathlib.Path('/home/jam/Documents')

TEMPLATE_FILE_PATH = pathlib.Path('template.conf').resolve()

DEFAULT_DOMAIN_NAME = 'ktep-inside.local'

SITES_DIRECTORY_PATH = pathlib.Path('/web/sites/kinside')

CERTIFICATE_SUBJECT = {
	'CN': 'KInsideAdmin',
	'O': 'KTEP',
	'OU': 'KInside',
	'C': 'RU',
	'ST': 'Kaluga region',
	'L': 'Kaluga',
	'emailAddress': 'ktep-inside@mail.ru',
}

NGINX_ROOT_PATH = pathlib.Path('/etc/nginx')

NGINX_SITES_AVAILABLE_PATH = NGINX_ROOT_PATH / 'sites-available'

NGINX_CERTIFICATES_PATH = NGINX_ROOT_PATH / 'certs'


def create_directory_in_documents(subdomain: str) -> None:
	path = DOCUMENTS_DIRECTORY_PATH / subdomain
	path.mkdir(exist_ok=True)


def create_config(
	subdomain: str,
	domain: str,
) -> None:
	path = resolve_config_file_path(subdomain, domain)
	content = generate_config_from_template(domain, subdomain)
	path.write_text(content)


def resolve_config_file_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	name = f'{subdomain}.{domain}'
	return NGINX_SITES_AVAILABLE_PATH / name


def generate_config_from_template(
	subdomain: str,
	domain: str,
) -> str:
	content = TEMPLATE_FILE_PATH.read_text()
	rendered_content = content.format(domain=domain, subdomain=subdomain)
	return rendered_content


def create_logs_directory(
	subdomain: str,
	domain: str,
) -> None:
	path = resolve_logs_directory_path(subdomain, domain)
	path.mkdir(parents=True, exist_ok=True)


def resolve_logs_directory_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	site_directory = f'{subdomain}.{domain}'
	return SITES_DIRECTORY_PATH / site_directory / 'logs'


def create_certificate(
	subdomain: str,
	domain: str,
) -> None:
	path = resolve_certificate_file_path(subdomain, domain)
	key_path = resolve_certificate_key_file_path(subdomain, domain)
	subject = generate_certificate_subject()
	run_openssl(path, key_path, subject)


def resolve_certificate_file_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	name = f'{subdomain}.{domain}.crt'
	return NGINX_CERTIFICATES_PATH / name


def resolve_certificate_key_file_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	name = f'{subdomain}.{domain}.key'
	return NGINX_CERTIFICATES_PATH / name


def generate_certificate_subject() -> str:
	string = ''
	for key, value in CERTIFICATE_SUBJECT.items():
		string += f'/{key}={value}'
	return string


def run_openssl(
	certificate_file_path: pathlib.Path,
	certificate_key_file_path: pathlib.Path,
	subject_string: str,
) -> None:
	subprocess.run([
		'openssl', 'req',
		'-x509',
		'-nodes',
		'-days', '365',
		'-newkey', 'rsa:2048',
		'-out', certificate_key_file_path,
		'-keyout', certificate_file_path,
		'-subj', subject_string,
	])


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'subdomain',
	)
	parser.add_argument(
		'-d',
		'--domain',
		default=DEFAULT_DOMAIN_NAME,
	)
	return parser.parse_args()


def main():
	args = parse_args()
	subdomain = args.subdomain
	domain = args.domain

	create_directory_in_documents(subdomain)
	create_config(subdomain, domain)
	create_logs_directory(subdomain, domain)
	create_certificate(subdomain, domain)


if __name__ == '__main__':
	main()
