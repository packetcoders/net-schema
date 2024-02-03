import json
import sys

import yaml
from rich import print as rprint  # noqa

# Load YAML or JSON


def load_yaml_or_json(filename):
    try:
        if filename.suffix in [".yaml", ".yml"]:
            with filename.open() as f:
                return yaml.safe_load(f)
        elif filename.suffix == ".json":
            with filename.open() as f:
                return json.load(f)
    except FileNotFoundError:
        rprint(f"[ERROR] File not found: {filename}")
        sys.exit(1)
