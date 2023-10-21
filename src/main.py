# The `ValidationRunner` class is responsible for loading a schema and definitions, validating
# documents against the schema, and logging any errors.
import pathlib
import sys

from rich import print as rprint

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

import logging
from pathlib import Path


from helpers import load_yaml_or_json
from src.plugins.json_schema.validator import JSONSchemaValidator


class ValidationRunner:
    def __init__(self, document_path, schema_path, validator, definition_paths=[]):
        self.validator = validator
        self.document_path = Path(document_path)
        self.schema_path = Path(schema_path)
        self.definition_paths = [
            Path(path) for path in definition_paths if path is not None
        ]

    def load_schema(self):
        return load_yaml_or_json(self.schema_path)

    def load_definitions(self):
        definitions = {}
        for def_path in self.definition_paths:
            for definition_file in def_path.iterdir():
                if definition_file.suffix in [".yaml", ".yml", ".json"]:
                    rootname = definition_file.stem
                    definitions[rootname] = load_yaml_or_json(definition_file)
        return definitions

    def validate_documents(self):
        errors = []
        for filename in self.document_path.iterdir():
            if filename.suffix in [".yaml", ".yml", ".json"]:
                host_vars_data = load_yaml_or_json(filename)
                file_errors = self.validator.errors(host_vars_data, self.schema)

                if file_errors:
                    for error in file_errors:
                        logging.error(
                            f"Error in file {filename.name}: {error['error']}"
                        )
                        rprint(
                            f":cross_mark: File: {filename.name} Error: {error['error']}"
                        )
                    errors.extend(file_errors)
                else:
                    logging.info(f"File {filename.name} validated successfully.")
                    rprint(f"File: {filename.name} - No validation errors found!")
        return errors

    def run(self):
        schema = self.load_schema()
        self.schema = schema
        definitions = self.load_definitions()
        self.validator.setup(schema, definitions)
        return self.validate_documents()


if __name__ == "__main__":
    runner = ValidationRunner(
        document_path="examples/host_vars",
        schema_path="examples/schema.yaml",
        validator=JSONSchemaValidator(),
        definition_paths=[],
    )
    runner.run()
