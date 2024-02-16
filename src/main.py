#! /usr/bin/env python

import pathlib
import sys
from pathlib import Path

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from typing import Union

import click
from rich import box
from rich.console import Console
from rich.table import Table

from src.plugins.json_schema.validator import JSONSchemaValidator

from .helpers import check_for_duplicate_keys, load_yaml_or_json


class SchemaValidator:
    """Validate a directory of YAML and JSON files against a schema."""

    def __init__(
        self,
        document_path: str,
        schema: str,
        validator: Union[JSONSchemaValidator],
        check_dup_keys: bool = False,
    ):
        """Initialize the SchemaValidator class."""
        self._validator = validator
        self._document_path = Path(document_path)
        self._schema = load_yaml_or_json(schema)
        self._errors = []
        self._check_dup_keys = check_dup_keys

    def initialize(self) -> None:
        """Initialize the validator and schema."""
        self._validator.initialize(self._schema)

    def _validate(self) -> dict:
        """Validates the documents."""
        for filename in self._document_path.iterdir():
            if filename.suffix in [".yaml", ".yml", ".json"]:
                data = filename.read_text()

                if self._check_dup_keys:
                    valid, error, key = check_for_duplicate_keys(data, filename.suffix[1:])
                    if not valid:
                        self._errors.append(
                            {
                                "error": True,
                                "msg": error,
                                "key": key,
                                "filename": str(filename),
                            }
                        )

                data = load_yaml_or_json(str(filename))
                errors = self._validator._validate(data)
                for e in errors:
                    e.update({"filename": str(filename)})
                    self._errors.append(e)

        return {"errors": self._errors}

    @property
    def results(self) -> list:
        """Return the validation results."""
        return self._validate()


@click.command()
@click.option(
    "--document_path",
    "-p",
    type=click.Path(),
    required=True,
    help="Path to the documents directory",
)
@click.option(
    "--schema",
    "-s",
    type=click.Path(),
    required=True,
    help="Path to the schema file",
    default=f"{Path(__file__).parent}/schema.yml",
)
@click.option(
    "--check-dup-keys",
    "-k",
    is_flag=True,
    help="Check for duplicate keys in JSON or YAML documents",
)
def main(document_path: str, schema: str, check_dup_keys: bool):
    """Validate a directory of YAML and JSON files against a schema."""
    console = Console()

    table = Table(show_header=True, header_style="bold magenta", box=box.HORIZONTALS)
    table.add_column("Result")
    table.add_column("Filename")
    table.add_column("Key")
    table.add_column("Msg")

    schema_validator = SchemaValidator(
        document_path=document_path,
        schema=schema,
        validator=JSONSchemaValidator(),
        check_dup_keys=check_dup_keys,
    )
    schema_validator.initialize()
    errors = False

    validation_results = schema_validator.results
    errors = sorted(validation_results["errors"], key=lambda x: x["filename"])

    for error in errors:
        if error.get("error"):
            errors = True
            table.add_row(
                ":cross_mark:",
                error["filename"],
                error.get("key", "--"),
                error["msg"],
            )
        else:
            table.add_row(":white_heavy_check_mark:", error["filename"], "--", "--")

    console.print(table)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
