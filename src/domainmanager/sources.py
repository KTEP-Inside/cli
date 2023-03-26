import pathlib


SOURCES_ROOT_DIRECTORY = pathlib.Path('/home/jam/Documents')


def create_sources_directory(subdomain: str) -> None:
	path = SOURCES_ROOT_DIRECTORY / subdomain
	path.mkdir(exist_ok=True)
