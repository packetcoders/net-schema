import json
import sys

import yaml
from rich import print as rprint

# Load YAML or JSON


def load_yaml_or_json(filename):
    """
    Load a YAML or JSON file and return its contents.

    Args:
        filename (str): The path to the file.

    Returns
    -------
        dict: The contents of the file as a dictionary.

    Raises
    ------
        FileNotFoundError: If the file is not found.
    """
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
