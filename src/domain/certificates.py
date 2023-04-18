import pathlib
import subprocess


CERTIFICATES_DIRECTORY = pathlib.Path('/etc/nginx/certs')

ATTRIBUTES = {
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
	certificate_path = CERTIFICATES_DIRECTORY / f'{subdomain}.{domain}.crt'
	key_path = CERTIFICATES_DIRECTORY / f'{subdomain}.{domain}.key'
	subject_string = _generate_subject_string()

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


def _generate_subject_string() -> str:
	string = ''
	for key, value in ATTRIBUTES.items():
		string += f'/{key}={value}'
	return string
