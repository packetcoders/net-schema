import json
from pathlib import Path
from typing import Union

import yaml


# Load YAML or JSON
def load_yaml_or_json(filename: str) -> Union[dict, ValueError]:
    """Load a YAML or JSON file."""
    if isinstance(filename, str):
        filename = Path(filename)
        if filename.suffix in [".yaml", ".yml"]:
            with open(filename) as f:
                return yaml.safe_load(f)
        elif filename.suffix == ".json":
            with open(filename) as f:
                return json.load(f)
    else:
        raise ValueError("Input should be a string.")
