import logging
from urllib.parse import urljoin
from jsonschema.validators import extend
from jsonschema import Draft7Validator, FormatChecker, exceptions
from referencing import Registry
from referencing.jsonschema import DRAFT7

from src.validators.asn import (
    is_2byte_asn,
    is_4byte_asn,
    is_asn,
    is_asn_dot_notation,
    is_asn_int_notation,
    is_documentation,
    is_public,
    is_private,
    is_reserved,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="net_schema.log",
)

DEFAULT_ID = "http://packetcoders.io/schemas/main"


class JSONSchemaValidator:
    def __init__(self):
        self._internal_validator = None

    def initialize(self, main_schema, definitions=None):
        self.main_schema = main_schema
        self.main_id = self.main_schema.get("$id", DEFAULT_ID)
        self.main_resource = DRAFT7.create_resource(self.main_schema)
        self.registry = self._load_definitions(
            self.main_id, self.main_resource, definitions
        )
        self.validator = self._init_validator(self.main_schema, self.registry)
        self._load_validators()

    def _init_validator(self, main_schema, registry):
        return Draft7Validator(
            main_schema, format_checker=FormatChecker(), registry=registry
        )


    def _load_validators(self):
        return "Not implemented yet"

    def _load_definitions(self, main_id, main_resource, definitions):
        resources = [(main_id, main_resource)]
        if definitions:
            for rootname, definition in definitions.items():
                def_id = urljoin(main_id, rootname)
                resources.append((def_id, DRAFT7.create_resource(definition)))

        return Registry().with_resources(resources)

    def errors(self, data):
        errors = []
        try:
            for error in self.validator.iter_errors(data):
                errors.append(
                    {
                        "error": error.message,
                        "value": ", ".join([prop for prop in error.path]),
                    }
                )
        except exceptions._WrappedReferencingError as e:
            # Catch the exception and append a custom error message
            errors.append(
                {"error": f"Unresolved reference error: {str(e)}", "value": "N/A"}
            )
        return errors
