#! /usr/bin/env python

import pathlib
import sys
from pathlib import Path

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

import click
from rich import box
from rich.console import Console
from rich.table import Table

from src.helpers import load_yaml_or_json
from src.plugins.json_schema.validator import JSONSchemaValidator
from helpers import read_yaml



class SchemaValidator:
    """
    A class for validating documents against a schema using a validator engine.

    Args:
        document_path (str): The path to the directory containing the documents to validate.
        schema (str): The path to the schema file.
        validator_engine (ValidatorEngine): The validator engine to use for validation.

    Attributes
    ----------
        _validator (ValidatorEngine): The validator engine instance.
        _document_path (Path): The path to the document directory.
        _schema (Path): The path to the schema file.
        _errors (list): A list to store validation errors.

    Methods
    -------
        initialize(): Initializes the validator by loading the schema.
        _load_schema(): Loads the schema from the file.
        _validate(): Validates each document in the document directory against the schema.
        results: Returns the validation results.

    """

    def __init__(self, document_path, schema, validator_engine):
        self._validator = validator_engine
        self._document_path = Path(document_path)
        print(schema)
        self._schema = Path(schema)
        self._errors = []
        self._warnings = []

    def initialize(self):
        """Initializes the validator by loading the schema."""
        self._load_schema()
        self._validator.initialize(self._schema)

    def _load_schema(self):
        """Loads the schema from the file."""
        self._schema, _ = load_yaml_or_json(self._schema)

    def _validate(self):
        """
        Validates each document in the document directory against the schema.

        Returns
        -------
            list: A list of validation errors.
        """
        for filename in self._document_path.iterdir():
            if filename.suffix in [".yaml", ".yml", ".json"]:
                data, file_warnings = load_yaml_or_json(filename)
                file_errors = self._validator.results(data)
                for error in file_errors:
                    error["filename"] = str(filename)  # Add filename key to each error
                self._errors.extend(file_errors)
                self._warnings.extend(file_warnings)
        return {"errors": self._errors, "warnings": self._warnings}

    @property
    def results(self):
        """
        Returns the validation results.

        Returns
        -------
            list: A list of validation errors.
        """
        return self._validate()


@click.command()
@click.option(
    "--document_path",
    "-p",
    type=click.Path(),
    required=True,
    help="path",
)
@click.option(
    "--schema",
    "-s",
    type=click.Path(),
    required=True,
    help="schema",
    default=f"{Path(__file__).parent}/schema.yml",
)
def main(document_path, schema):
    """
    It iterates through the files in the directory and validates them.

    :param document_path: The path to the directory containing the YAML files to be validated
    :param schema: The path to the schema file
    """
    print(schema)
    schema = read_yaml(schema)

    console = Console()

    # Define the table
    table = Table(show_header=True, header_style="bold magenta", box=box.HORIZONTALS)
    table.add_column("Result")
    table.add_column("Msg")
    table.add_column("Value")
    table.add_column("Filename")

    schema_validator = SchemaValidator(
        document_path=document_path,
        schema=schema,
        validator_engine=JSONSchemaValidator(),
    )
    schema_validator.initialize()

    errors = False

    for error in schema_validator.results:
        if error["error"]:
            errors = True
            table.add_row(
                ":cross_mark:", error["msg"], error["value"], error["filename"]
            )
        else:
            table.add_row(
                ":white_heavy_check_mark:", "No errors", None, error["filename"]
            )

    # Display the table
    console.print(table)

    # If the validation result is false, then the program will exit with a status code of 1.
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
