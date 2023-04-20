from json import loads, dumps
from pathlib import Path
from typing import Dict, Any

def read_config(file: Path) -> Dict:
    return loads(file.read_text())


def write_config(file: Path, content: Any) -> None:
    return file.write_text(dumps(content, indent=2))
