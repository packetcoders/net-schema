import json
import logging
import sys
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
        print(f"[ERROR] File not found: {filename}")
        sys.exit(1)

