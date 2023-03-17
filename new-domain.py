#!/usr/bin/env python3
"""
1. Создать конфиг из шаблона в /etc/nginx/sites-available
2. Сгенерировать сертификат в /etc/nginx/certs
3. Создать папку с именем поддомена в ~/Documents
"""
import argparse
import pathlib
import subprocess


TEMPLATE_FILE = pathlib.Path('template.conf').resolve()
DEFAULT_DOMAIN = 'ktep-inside.local'
NGINX_ROOT_PATH = pathlib.Path('/etc/nginx')
NGINX_SITES_AVAILABLE_PATH = NGINX_ROOT_PATH / 'sites-available'
NGINX_CERTIFICATES_PATH = NGINX_ROOT_PATH / 'certs'
DOCUMENTS_FOLDER = pathlib.Path('/home/jam/Documents')


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'subdomain',
	)
	parser.add_argument(
		'-d',
		'--domain',
		default=DEFAULT_DOMAIN,
	)
	return parser.parse_args()


def create_config(domain: str, subdomain: str) -> None:
	file_name = f'{subdomain}.{domain}.conf'
	file_path = NGINX_SITES_AVAILABLE_PATH / file_name
	config_content = generate_config_from_template(domain, subdomain)
	file_path.write_text(config_content)


def create_certificates(domain: str, subdomain: str) -> None:
	key_file_name = f'{subdomain}.{domain}.key'
	key_file_path = NGINX_CERTIFICATES_PATH / key_file_name
	certificate_file_name = f'{subdomain}.{domain}.crt'
	certificate_file_path = NGINX_CERTIFICATES_PATH / certificate_file_name
	subprocess.run([
		'sudo', 'openssl', 'req', '-x509', '-nodes', '-days', '365', '-newkey', 'rsa:2048',
		'-keyout', key_file_path,
		'-out', certificate_file_path,
		'-subj',
		'/CN=KInsideAdmin/O=KTEP/OU=KInside/C=RU/ST=Kaluga region/L=Kaluga/emailAddress=ktep-inside@mail.ru',
	])


def create_folder_in_documents(subdomain: str) -> None:
	folder_path = DOCUMENTS_FOLDER / subdomain
	folder_path.mkdir(exist_ok=True)


def generate_config_from_template(domain: str, subdomain: str) -> str:
	template_content = TEMPLATE_FILE.read_text()
	rendered_content = template_content.format(domain=domain, subdomain=subdomain)
	return rendered_content


def main():
	args = parse_args()
	subdomain = args.subdomain
	domain = args.domain

	create_config(domain, subdomain)
	create_certificates(domain, subdomain)
	create_folder_in_documents(subdomain)


if __name__ == '__main__':
	main()
