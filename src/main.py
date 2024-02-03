import pathlib
import sys
from pathlib import Path

from rich import print as rprint

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from src.helpers import load_yaml_or_json
from src.plugins.json_schema.validator import JSONSchemaValidator


class SchemaValidator:
    def __init__(self, document_path, schema, validator_engine):
        self._validator = validator_engine
        self._document_path = Path(document_path)
        self._schema = Path(schema)
        self._errors = []

    def initialize(self):
        self._load_schema()
        self._validator.initialize(self._schema)

    def _load_schema(self):
        self._schema = load_yaml_or_json(self._schema)

    def _validate(self):
        for filename in self._document_path.iterdir():
            if filename.suffix in [".yaml", ".yml", ".json"]:
                data = load_yaml_or_json(filename)
                file_errors = self._validator.results(data)
                for error in file_errors:
                    error["filename"] = str(filename)  # Add filename key to each error
                self._errors.extend(file_errors)
        return self._errors

    @property
    def results(self):
        return self._validate()


def run():
    schema_validator = SchemaValidator(
        document_path="examples/host_vars",
        schema="examples/schema.yaml",
        validator_engine=JSONSchemaValidator(),
    )
    schema_validator.initialize()
    rprint(schema_validator.results)


if __name__ == "__main__":
    run()
