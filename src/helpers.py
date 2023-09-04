import json
import logging

import yaml

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="netschema.log",
)

# Load YAML or JSON
def load_yaml_or_json(filename):
    try:
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            with open(filename, "r") as f:
                return yaml.safe_load(f)
        elif filename.endswith(".json"):
            with open(filename, "r") as f:
                return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except Exception as e:
        logging.error(f"Error loading file: {filename} - {e}")
        raise e
