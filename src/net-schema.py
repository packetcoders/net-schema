# pip install references
import json
from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT7
from rich import print as rprint
from rich import inspect
from urllib.parse import urljoin
import os
import yaml
from helpers import load_yaml_or_json
import sys

MAIN_SCHEMA = "src/main_schema.json"
DEFAULT_ID = "http://example.com/schemas/main"


def init_main_schema():
    main_schema = load_yaml_or_json(MAIN_SCHEMA)
    main_resource = DRAFT7.create_resource(main_schema)
    return main_schema, main_resource


def init_registry(main_id, main_resource):
    resources = [(main_id, main_resource)]
    for filename in os.listdir("defs"):
        if filename.endswith(".json"):
            # Get the definition name by stripping the .json extension
            def_name = filename[:-5]
            def_id = urljoin(main_id, def_name)

            # Load the schema from the file
            with open(f"defs/{filename}") as f:
                definition = json.load(f)
                definition_resource = DRAFT7.create_resource(definition)

            # Add the definition ID and resource to the resources list
            resources.append((def_id, definition_resource))
    registry = Registry().with_resources(resources)
    return registry


def init_validator(main_schema, registry):
    validator = Draft7Validator(
        main_schema, format_checker=FormatChecker(), registry=registry
    )
    return validator


def init_json_schema_validator():
    main_schema, main_resource = init_main_schema()
    main_id = main_schema.get("$id", DEFAULT_ID)
    registry = init_registry(main_id, main_resource)
    return init_validator(main_schema, registry)


def main(document_path):
    # init JSON Schema and Registry
    validator = init_json_schema_validator()

    # Loop over the files in the 'host_vars' directory
    for filename in os.listdir(document_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            # Load the host_vars data from the file
            with open(f"{document_path}/{filename}", "r") as f:
                host_vars_data = yaml.safe_load(f)

            # Validate the loaded host_vars data against the main schema
            errors = list(validator.iter_errors(host_vars_data))
            if errors:
                for error in errors:
                    rprint(f":cross_mark: File: {filename} Error: {error.message}")
            else:
                rprint(f"File: {filename} - No validation errors found!")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main(document_path="examples/host_vars")
