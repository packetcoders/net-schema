import logging
import sys
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker, exceptions
from rich import print as rprint

sys.path.append(str(Path(__file__).parent.parent.parent))

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


CUSTOM_VALIDATORS = {**ASN_VALIDATORS}


class JSONSchemaValidator:
    def initialize(self, schema):
        self._validator = Draft7Validator(schema, format_checker=FormatChecker())
        self._load_custom_validators()
        self._errors = []

    def _load_custom_validators(self):
        self._validator.VALIDATORS.update(CUSTOM_VALIDATORS)

    def _validate(self, data):
        self._errors = []

        if self._validator.is_valid(data):
            self._errors.append({"error": False, "msg": None, "value": None})
        else:
            try:
                for error in self._validator.iter_errors(data):
                    self._errors.append(
                        {
                            "error": True,
                            "msg": error.message,
                            "value": ", ".join([prop for prop in error.path])
                            if error.path
                            else None,
                        }
                    )
            except exceptions._WrappedReferencingError as e:
                self._errors.append(
                    {
                        "error": True,
                        "msg": f"Unresolved reference error: {str(e)}",
                        "value": None,
                    }
                )
            except Exception as e:
                self._errors.append(
                    {
                        "error": True,
                        "msg": f"Unknown error: {str(e)}",
                        "value": None,
                    }
                )
        return self._errors

    def results(self, data):
        return self._validate(data)


if __name__ == "__main__":
    schema = {
        "type": "object",
        "properties": {"asn": {"type": "string", "asn": True}},
        "required": ["asn"],
    }
    data = {"asn": "4294967296"}

    schema_validator = JSONSchemaValidator()
    schema_validator.initialize(schema=schema)
    rprint(schema_validator.results(data))
