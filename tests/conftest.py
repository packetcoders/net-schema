"""Module contains fixtures and utilities for testing JSON schema validation."""

import sys
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, FormatChecker

sys.path.append(f"{Path(__file__).parent.parent}/src")

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
from plugins.json_schema.ip import (
    ip,
    ip_ipv4,
    ip_ipv6,
    ip_linklocal,
    ip_multicast,
    ip_private,
    ip_reserved,
)
from plugins.json_schema.vlan import vlan, vlan_extended, vlan_standard

ASN_VALIDATORS = {
    "asn_public": asn_public,
    "asn_private": asn_private,
    "asn_reserved": asn_reserved,
    "asn_documentation": asn_documentation,
    "asn_2byte": asn_2byte,
    "asn_4byte": asn_4byte,
    "asn": asn,
    "asn_dot-notation": asn_notation_dot,
    "asn_int-notation": asn_notation_int,
}

IP_VALIDATORS = {
    "ip": ip,
    "ip_ipv4": ip_ipv4,
    "ip_ipv6": ip_ipv6,
    "ip_multicast": ip_multicast,
    "ip_private": ip_private,
    "ip_reserved": ip_reserved,
    "ip_linklocal": ip_linklocal,
}

VLAN_VALIDATORS = {
    "vlan": vlan,
    "vlan_standard": vlan_standard,
    "vlan_extended": vlan_extended,
}

VALIDATORS = {**ASN_VALIDATORS, **IP_VALIDATORS, **VLAN_VALIDATORS}


@pytest.fixture(scope="session")
def basic_validator():
    """
    Fixture that returns a basic JSON schema validator.

    This validator uses the Draft7Validator from the jsonschema library
    and includes additional custom validators from the ASN_VALIDATORS, IP_VALIDATORS, and VLAN_VALIDATORS dictionaries.

    Returns
    -------
        function: A function that can be used to validate JSON schemas.
    """

    def _basic_validator(schema):
        v = Draft7Validator(schema=schema, format_checker=FormatChecker())
        Draft7Validator.VALIDATORS.update(VALIDATORS)
        return v

    return _basic_validator
