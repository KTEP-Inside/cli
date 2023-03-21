import pathlib


ROOT_PATH = pathlib.Path(__file__).parent

TEMPLATE_FILE =  ROOT_PATH / 'template.conf'

DEFAULT_CONFIG_OUT_DIRECTORY = pathlib.Path('/etc/nginx/sites-available')

FILE_NAME_TEMPLATE = '{subdomain}.{domain}.conf'


class NginxConfigGenerator:
	domain: str
	subdomain: str
	out_directory: pathlib.Path

	def __init__(
		self,
		domain: str,
		subdomain: str,
		out_directory: pathlib.Path = DEFAULT_CONFIG_OUT_DIRECTORY,
	) -> None:
		self.domain = domain
		self.subdomain = subdomain
		self.out_directory = out_directory

	def generate(self) -> None:
		path = self.resolve_file_path()
		content = self.render_template()
		self.write_config(path, content)

	def resolve_file_path(self) -> pathlib.Path:
		name = self.resolve_file_name()
		return self.out_directory / name

	def resolve_file_name(self) -> str:
		return FILE_NAME_TEMPLATE.format(
			subdomain=self.subdomain,
			domain=self.domain,
		)

	def render_template(self) -> str:
		content = TEMPLATE_FILE.read_text()
		return content.format(domain=self.domain, subdomain=self.subdomain)

	def write_config(self, path: pathlib.Path, content: str) -> None:
		path.touch(exist_ok=True)
		path.write_text(content)
