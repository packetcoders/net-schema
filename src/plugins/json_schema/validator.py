import logging
from urllib.parse import urljoin

from jsonschema import Draft7Validator, FormatChecker, exceptions
from jsonschema.validators import extend
from referencing import Registry
from referencing.jsonschema import DRAFT7

from plugins.json_schema.asn import (
    asn,
    asn_2byte,
    asn_4byte,
    asn_documentation,
    asn_notation_dot,
    asn_notation_int,
    asn_private,
    asn_public,
    asn_reserved,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="net_schema.log",
)


DEFAULT_ID = "http://packetcoders.io/schemas/main"

ASN_VALIDATORS = {
    "public": asn_public,
    "private": asn_private,
    "reserved": asn_reserved,
    "documentation": asn_documentation,
    "2byte": asn_2byte,
    "4byte": asn_4byte,
    "asn": asn,
    "dot-notation": asn_notation_dot,
    "int-notation": asn_notation_int,
}


VALIDATORS = {**ASN_VALIDATORS}


class JSONSchemaValidator:
    def __init__(self):
        """Initialize the validator."""
        self._internal_validator = None

    def setup(self, main_schema, definitions=None):
        self.main_schema = main_schema
        self.main_id = self.main_schema.get("$id", DEFAULT_ID)
        self.main_resource = DRAFT7.create_resource(self.main_schema)

        self.registry = self._load_definitions(
            self.main_id, self.main_resource, definitions
        )
        self.validator = self._create_validator_instance(
            self.main_schema, self.registry
        )

    def _create_validator_instance(self, main_schema, registry):
        validator_class = extend(Draft7Validator, validators=VALIDATORS)
        return validator_class(
            main_schema, format_checker=FormatChecker(), registry=registry
        )

    def _load_definitions(self, main_id, main_resource, definitions):
        resources = [(main_id, main_resource)]
        if definitions:
            for rootname, definition in definitions.items():
                def_id = urljoin(main_id, rootname)
                resources.append((def_id, DRAFT7.create_resource(definition)))

        return Registry().with_resources(resources)

    def errors(self, data, schema):
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
            errors.append(
                {"error": f"Unresolved reference error: {str(e)}", "value": "N/A"}
            )
        return errors
