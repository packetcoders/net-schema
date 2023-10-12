import logging
from urllib.parse import urljoin

from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT7
from rich import inspect

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="net_schema.log",
)

DEFAULT_ID = "http://packetcoders.io/schemas/main"


class JSONSchemaValidator:
    def __init__(self, main_schema, definitions=None):
        self.main_schema = main_schema
        self.main_id = self.main_schema.get("$id", DEFAULT_ID)
        self.main_resource = DRAFT7.create_resource(self.main_schema)
        self.registry = self._load_definitions(self.main_id, self.main_resource, definitions)
        self.validator = self._init_validator(self.main_schema, self.registry)

    def _load_definitions(self, main_id, main_resource, definitions):
        resources = [(main_id, main_resource)]
        if definitions:
            for rootname, definition in definitions.items():
                def_id = urljoin(main_id, rootname)
                resources.append((def_id, DRAFT7.create_resource(definition)))

        return Registry().with_resources(resources)

    def _init_validator(self, main_schema, registry):
        return Draft7Validator(
            main_schema, format_checker=FormatChecker(), registry=registry
        )

    def validate(self, data):
        errors = [error for error in self.validator.iter_errors(data)]
        return errors

    def errors(self, data):
        errors = []
        for error in self.validator.iter_errors(data):
            errors.append(
                {
                    "error": error.message,
                    "value": ", ".join([prop for prop in error.path]),
                }
            )
        return errors


# Usage example
if __name__ == "__main__":
    # Main schema and definitions
    schema = {
        "$id": "http://example.com/schema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0}
        },
        "required": ["name"]
    }

    definitions = {
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"}
            },
            "required": ["street", "city"]
        }
    }

    validator = JSONSchemaValidator(schema, definitions)
    data = {
        "name": "John",
        "age": -5
    }
    errors = validator.errors(data)
    print(errors)