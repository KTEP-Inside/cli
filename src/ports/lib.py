from shared.lib import read_config

from .config import PORTS_CONFIG
from .types import PortsConfig


def read_ports_config() -> PortsConfig:
    return read_config(PORTS_CONFIG)
