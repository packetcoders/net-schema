import json

import yaml


# Load YAML or JSON
def load_yaml_or_json(filename):
    if filename.endswith(".yaml") or filename.endswith(".yml"):
        with open(filename, "r") as f:
            return yaml.safe_load(f)
    elif filename.endswith(".json"):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        raise Exception(f"Unknown file type for {filename}")
