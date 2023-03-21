import pathlib
import subprocess


DEFAULT_CERTIFICATE_OUT_DIRECTORY = pathlib.Path('/etc/nginx/certs')

CERTIFICATE_FILE_NAME_TEMPLATE = '{subdomain}.{domain}.crt'

KEY_FILE_NAME_TEMPLATE = '{subdomain}.{domain}.key'

ATTRIBUTES = {
	'CN': 'KInsideAdmin',
	'O': 'KTEP',
	'OU': 'KInside',
	'C': 'RU',
	'ST': 'Kaluga region',
	'L': 'Kaluga',
	'emailAddress': 'ktep-inside@mail.ru',
}


class OpenSSLSertificateGenerator:
	domain: str
	subdomain: str
	out_directory: pathlib.Path

	def __init__(
		self,
		domain: str,
		subdomain: str,
		out_directory: pathlib.Path = DEFAULT_CERTIFICATE_OUT_DIRECTORY,
	) -> None:
		self.domain = domain
		self.subdomain = subdomain
		self.out_directory = out_directory

	def generate(self) -> None:
		certificate_path = self.resolve_certificate_file_path()
		key_path = self.resolve_key_file_path()
		subject_string = self.create_subject_string()
		self.run_openssl(certificate_path, key_path, subject_string)

	def resolve_certificate_file_path(self) -> pathlib.Path:
		name = self.resolve_certificate_file_name()
		return self.out_directory / name

	def resolve_certificate_file_name(self) -> str:
		return CERTIFICATE_FILE_NAME_TEMPLATE.format(
			subdomain=self.subdomain,
			domain=self.domain,
		)

	def resolve_key_file_path(self) -> pathlib.Path:
		name = self.resolve_key_file_name()
		return self.out_directory / name

	def resolve_key_file_name(self) -> str:
		return KEY_FILE_NAME_TEMPLATE.format(
			subdomain=self.subdomain,
			domain=self.domain,
		)

	def create_subject_string(self) -> str:
		string = ''
		for key, value in ATTRIBUTES.items():
			string += f'/{key}={value}'
		return string

	def run_openssl(
		self,
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
