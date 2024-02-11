#! /usr/bin/env python

import pathlib
import sys
from pathlib import Path

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

import click
from helpers import load_yaml_or_json
from rich import box
from rich.console import Console
from rich.table import Table

from src.plugins.json_schema.validator import JSONSchemaValidator


class SchemaValidator:
    """A class to validate a directory of YAML files against a schema."""

    def __init__(self, document_path, schema, validator):
        """Initializes the SchemaValidator class."""
        self._validator = validator
        self._document_path = Path(document_path)
        self._schema = load_yaml_or_json(schema)
        self._errors = []

    def initialize(self) -> None:
        """Initializes the validator by loading the schema."""
        self._validator.initialize(self._schema)

    def _validate(self) -> dict:
        """Validates the YAML files in the directory."""
        for filename in self._document_path.iterdir():
            if filename.suffix in [".yaml", ".yml", ".json"]:
                filename = str(filename)
                errors = self._validator.results(load_yaml_or_json(filename))
                for e in errors:
                    e.update({"filename": str(filename)})
                    self._errors.append(e)
        return {"errors": self._errors}

    @property
    def results(self) -> list:
        """Returns the validation results."""
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
def main(document_path: str, schema: str):
    """Main function."""
    console = Console()

    table = Table(show_header=True, header_style="bold magenta", box=box.HORIZONTALS)
    table.add_column("Result")
    table.add_column("Msg")
    table.add_column("key")
    table.add_column("Filename")

    schema_validator = SchemaValidator(
        document_path=document_path,
        schema=schema,
        validator=JSONSchemaValidator(),
    )
    schema_validator.initialize()
    errors = False

    errors = sorted(schema_validator.results["errors"], key=lambda x: x["filename"])

    for error in errors:
        if error["error"]:
            errors = True
            table.add_row(":cross_mark:", error["msg"], error["key"], error["filename"])
        else:
            table.add_row(":white_heavy_check_mark:", "No errors", None, error["filename"])

    console.print(table)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
