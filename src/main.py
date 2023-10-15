import logging
import json
import yaml
from urllib.parse import urljoin
from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT7
from pathlib import Path
from rich import inspect, print as rprint  # renaming to avoid conflict with built-in print
import sys
from rich import print as rprint

import pathlib
import sys


sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from src.json_schema import JSONSchemaValidator
from helpers import load_yaml_or_json
from runner import ValidationRunner



if __name__ == "__main__":
    runner = ValidationRunner(
        document_path="examples/host_vars",
        schema_path="examples/schema.yaml",
        validator=JSONSchemaValidator(),
        definition_paths=["examples/custom_defs"],
    )
    runner.run()