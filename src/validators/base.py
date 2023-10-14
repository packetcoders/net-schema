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

#sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from .abstracts import AbstractValidator
from helpers import load_yaml_or_json


class BaseValidator(AbstractValidator):

    def __init__(self, document_path, schema_path, *definition_paths):
        self.document_path = Path(document_path)
        self.schema_path = Path(schema_path)
        self.definition_paths = [Path(path) for path in definition_paths]

    def load_schema(self):
        return load_yaml_or_json(self.schema_path)

    def load_definitions(self):
        definitions = {}
        for def_path in self.definition_paths:
            for definition_file in def_path.iterdir():
                if definition_file.suffix in ['.yaml', '.yml', '.json']:
                    rootname = definition_file.stem
                    definitions[rootname] = load_yaml_or_json(definition_file)
        rprint(definitions)
        return definitions

    def validate_documents(self, validator):
        errors = []
        for filename in self.document_path.iterdir():
            if filename.suffix in ['.yaml', '.yml', '.json']:
                host_vars_data = load_yaml_or_json(filename)
                file_errors = validator.errors(host_vars_data)

                if file_errors:
                    for error in file_errors:
                        logging.error(f"Error in file {filename.name}: {error['error']}")
                        rprint(f":cross_mark: File: {filename.name} Error: {error['error']}")
                    errors.extend(file_errors)
                else:
                    logging.info(f"File {filename.name} validated successfully.")
                    rprint(f"File: {filename.name} - No validation errors found!")
        return errors

    def initialize_validator(self, main_schema, definitions):
        return None

    def run(self):
        main_schema = self.load_schema()
        definitions = self.load_definitions()
        validator = self.initialize_validator(main_schema, definitions)
        errors = self.validate_documents(validator)
        if errors:
            sys.exit(1)




