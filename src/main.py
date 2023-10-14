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

from validators.json_schema import JSONSchemaValidator



if __name__ == "__main__":
    runner = JSONSchemaValidator(
        document_path="examples/host_vars",
        schema_path="examples/schema.yaml",
        def_path_custom="examples/custom_defs",
        def_path_builtin="builtin_defs"
    )
    runner.run()