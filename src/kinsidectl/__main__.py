from config.constants import CONFIG_DIR
from .cli import cli


__version__ = "0.1.0"


def main():
    cli()


if __name__ == "__main__":
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    main()
