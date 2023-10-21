import logging
from urllib.parse import urljoin

from jsonschema import Draft7Validator, FormatChecker, exceptions
from jsonschema.validators import extend
from referencing import Registry
from referencing.jsonschema import DRAFT7

from plugins.json_schema.asn import (
    is_2byte_asn,
    is_4byte_asn,
    is_asn,
    is_asn_dot_notation,
    is_asn_int_notation,
    is_documentation,
    is_private,
    is_public,
    is_reserved,
)
from plugins.json_schema.ip import (
    is_documentation,
    is_ip_interface,
    is_ipaddress,
    is_ipv4,
    is_ipv6,
    is_link_local,
    is_loopback,
    is_multicast,
    is_network,
    is_private,
    is_reserved,
    is_shared,
    is_unspecified,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="net_schema.log",
)


DEFAULT_ID = "http://packetcoders.io/schemas/main"

ASN_VALIDATORS = {
    "public-asn": is_public,
    "private-asn": is_private,
    "reserved-asn": is_reserved,
    "documentation-asn": is_documentation,
    "2byte-asn": is_2byte_asn,
    "4byte-asn": is_4byte_asn,
    "asn": is_asn,
    "asn-dot-notation": is_asn_dot_notation,
    "asn-int-notation": is_asn_int_notation,
}

IP_VALIDATORS = {
    "multicast": is_multicast,
    "private": is_private,
    "unspecified": is_unspecified,
    "reserved": is_reserved,
    "loopback": is_loopback,
    "link-local": is_link_local,
    "ipv4": is_ipv4,
    "ipv6": is_ipv6,
    "ip-address": is_ipaddress,
    "ip-network": is_network,
    "ip-interface": is_ip_interface,
    "shared": is_shared,
    "documentation": is_documentation,
}


VALIDATORS = {**ASN_VALIDATORS, **IP_VALIDATORS}


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
        self.validator = self._create_validator_instance(self.main_schema, self.registry)

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
            for error in self.validator.iter_errors(schema, data):
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
