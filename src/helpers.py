import json
from pathlib import Path
from typing import Union

import yaml


class DuplicateKeyError(ValueError):
    """Custom exception for duplicate keys."""

    def __init__(self, message, key):
        """Initialize the exception."""
        super().__init__(message)
        self.key = key


class SafeCustomYamlLoader(yaml.SafeLoader):
    """Custom YAML loader to check for duplicate keys."""

    def construct_mapping(self, node, deep=False):
        """Construct a mapping."""
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise DuplicateKeyError(f"Duplicate key found: {key}", key)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


def json_object_pairs_hook(pairs):
    """Custom object pairs hook for JSON."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"Duplicate key found: {key}", key)
        result[key] = value
    return result


def check_for_duplicate_keys(data, file_format):
    """Check for duplicate keys in a JSON or YAML file."""
    try:
        if file_format == "json":
            json.loads(data, object_pairs_hook=json_object_pairs_hook)
        elif file_format in ["yaml", "yml"]:
            # Use yaml.load() with the correct custom loader
            yaml.load(data, Loader=SafeCustomYamlLoader)  # noqa : SafeLoader is used
        return True, None, None
    except DuplicateKeyError as e:
        return False, str(e), e.key


def load_yaml_or_json(filename: str) -> Union[dict, ValueError]:
    """Load a YAML or JSON file."""
    if isinstance(filename, str):
        filename_path = Path(filename)
        if filename_path.suffix in [".yaml", ".yml"]:
            with open(filename_path) as f:
                return yaml.safe_load(f)
        elif filename_path.suffix == ".json":
            with open(filename_path) as f:
                return json.load(f)
    else:
        raise ValueError("Input should be a string.")
