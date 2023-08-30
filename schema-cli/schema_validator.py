#!/usr/bin/env python3

import os
import sys
from pathlib import Path

import click
import yaml
from jsonschema import Draft7Validator, FormatChecker
from rich import box
from rich import print as rprint, inspect
from rich.console import Console
from rich.table import Table


def read_yaml(filename):
    """
    It opens the file, reads the contents, and returns the result of parsing the contents as YAML

    :param filename: The name of the file to read
    :return: A dictionary
    """
    with open(filename) as file:
        return yaml.safe_load(file)


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
    It iterates through the files in the directory and validates them

    :param document_path: The path to the directory containing the YAML files to be validated
    :param schema: The path to the schema file
    """

    schema = read_yaml(schema)

    ext = ("yaml", "yml")

    console = Console()

    # Define the table
    table = Table(show_header=True, header_style="bold magenta", box=box.HORIZONTALS)
    table.add_column("Result", width=12)
    table.add_column("Filename", width=30)
    table.add_column(
        "Error",
    )

    format_checker = FormatChecker()
    validator = Draft7Validator(schema, format_checker=format_checker)

    # Iterating through the files in the directory and validating them.
    for file in os.listdir(document_path):
        if file.endswith(ext):
            document = read_yaml(f"{document_path}/{file}")
            errors = validator.iter_errors(document)
            for error in errors:
                inspect(error)
                table.add_row(":cross_mark:", f"{document_path}/{file}", error.message)

    # Display the table
    console.print(table)

    # If the validation result is false, then the program will exit with a status code of 1.
    if errors:
        sys.exit(1)


# This is a common idiom to check if the script is being run directly, or being imported from another
# module.
if __name__ == "__main__":
    # The entry point of the program.
    main()
