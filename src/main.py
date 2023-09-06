#!/usr/bin/env python3

import logging
import os
import sys

import yaml
from rich import print as rprint
from typer import Option, Typer

from net_schema import init_json_schema_validator

app = Typer()


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="netschema.log",
)


@app.command()
def main(
    document_path: str = Option(
        "examples/host_vars",
        help="Path to the directory containing documents to validate.",
    ),
    schema: str = Option("examples/schema.json", help="Path to the main schema file."),
    def_path: str = Option(
        "examples/defs", help="Path to the directory containing custom definitions."
    ),
):
    """
    Validates YAML files in the document_path directory against the JSON schema.
    """
    logging.debug("✅ Starting validation process.")
    validator = init_json_schema_validator(schema, def_path)
    errors = []

    for filename in os.listdir(document_path):
        if filename.endswith((".yaml", ".yml")):
            with open(os.path.join(document_path, filename), "r") as f:
                host_vars_data = yaml.safe_load(f)

            file_errors = list(validator.iter_errors(host_vars_data))

            if file_errors:
                for error in file_errors:
                    logging.error(f"Error in file {filename}: {error.message}")
                    rprint(f":cross_mark: File: {filename} Error: {error.message}")
                errors.extend(file_errors)
            else:
                logging.info(f"File {filename} validated successfully.")
                rprint(f"File: {filename} - No validation errors found!")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    app()
