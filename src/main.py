import pathlib
import sys
from pathlib import Path

from rich import print as rprint

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from src.helpers import load_yaml_or_json
from src.plugins.json_schema.validator import JSONSchemaValidator


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


def run():
    """
    Runs the schema validation process.

    This function initializes a SchemaValidator object, sets the document path,
    schema, and validator engine, and then runs the validation process. Finally,
    it prints the validation results.

    """
    schema_validator = SchemaValidator(
        document_path="examples/host_vars",
        schema="examples/schema.yaml",
        validator_engine=JSONSchemaValidator(),
    )
    schema_validator.initialize()
    rprint(schema_validator.results)


if __name__ == "__main__":
    run()
