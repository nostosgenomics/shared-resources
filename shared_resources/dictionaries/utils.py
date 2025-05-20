import json
from pathlib import Path
from typing import Union


def load_json(json_file: Union[str, Path]) -> Union[dict, list]:
    with Path(json_file).open() as f:
        contents = json.load(f)
    return contents
