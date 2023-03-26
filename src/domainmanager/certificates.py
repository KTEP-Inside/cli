import pathlib
import subprocess


CERTIFICATES_DIRECTORY = pathlib.Path('/etc/nginx/certs')

CERTIFICATE_NAME_TEMPLATE = '{subdomain}.{domain}.crt'

KEY_NAME_TEMPLATE = '{subdomain}.{domain}.key'

CERTIFICATE_SUBJECT = {
	'CN': 'KInsideAdmin',
	'O': 'KTEP',
	'OU': 'KInside',
	'C': 'RU',
	'ST': 'Kaluga region',
	'L': 'Kaluga',
	'emailAddress': 'ktep-inside@mail.ru',
}


def create_ssl_certificate(
	subdomain: str,
	domain: str,
) -> None:
	path = _resolve_certificate_path(subdomain, domain)
	key_path = _resolve_key_path(subdomain, domain)
	subject = _generate_subject_string()
	_run_openssl(path, key_path, subject)


def _resolve_certificate_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	name = CERTIFICATE_NAME_TEMPLATE.format(subdomain=subdomain, domain=domain)
	return CERTIFICATES_DIRECTORY / name


def _resolve_key_path(
	subdomain: str,
	domain: str,
) -> pathlib.Path:
	name = KEY_NAME_TEMPLATE.format(subdomain=subdomain, domain=domain)
	return CERTIFICATES_DIRECTORY / name


def _generate_subject_string() -> str:
	string = ''
	for key, value in CERTIFICATE_SUBJECT.items():
		string += f'/{key}={value}'
	return string


def _run_openssl(
	certificate_path: pathlib.Path,
	key_path: pathlib.Path,
	subject_string: str,
) -> None:
	subprocess.run([
		'openssl', 'req',
		'-x509',
		'-nodes',
		'-days', '365',
		'-newkey', 'rsa:2048',
		'-out', certificate_path,
		'-keyout', key_path,
		'-subj', subject_string,
	])
