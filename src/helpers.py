import json
import sys
from typing import List

import yaml
from rich import print as rprint

current_file = None  # Global variable to hold the current file being processed


class UniqueKeyLoader(yaml.SafeLoader):
    warnings: List[dict] = []

    @classmethod
    def add_warning(cls, warning_msg, key, value, filename):
        cls.warnings.append(
            {"warning": True, "msg": warning_msg, "key": key, "filename": str(filename)}
        )

    def construct_mapping(self, node, deep=False):
        mapping = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                warning_msg = f"Duplicate keys '{key}' found in YAML file."
                UniqueKeyLoader.add_warning(
                    warning_msg, key, self.construct_object(value_node), current_file
                )
            mapping.add(key)
        return super().construct_mapping(node, deep)


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

    global current_file
    current_file = filename

    try:
        if filename.suffix in [".yaml", ".yml"]:
            with filename.open() as f:
                UniqueKeyLoader.warnings = []  # Reset warnings before loading
                data = yaml.load(f, Loader=UniqueKeyLoader)
                warnings = UniqueKeyLoader.warnings
                return data, warnings
        elif filename.suffix == ".json":
            with filename.open() as f:
                return json.load(f), []
    except FileNotFoundError:
        rprint(f"[ERROR] File not found: {filename}")
        sys.exit(1)
