import json
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

VALIDATORS = {**ASN_VALIDATORS}
ASN_FIXTURE = f"{Path(__file__).parent}/fixtures/asn.json"
ASN_FIXTURE_CHECKS = ["asn_min", "asn_max"]


@pytest.fixture(scope="session")
def asn_fixture():
    with open(ASN_FIXTURE) as file:
        data = json.load(file)
    return data


@pytest.fixture(scope="session")
def basic_validator():
    def _basic_validator(schema):
        v = Draft7Validator(schema=schema, format_checker=FormatChecker())
        Draft7Validator.VALIDATORS.update(VALIDATORS)
        return v

    return _basic_validator


@pytest.mark.parametrize("check", ASN_FIXTURE_CHECKS)
def test_asn_validators_valid(basic_validator, check, asn_fixture):
    schema = asn_fixture[check]["schema"]
    data = asn_fixture[check]["data"]["valid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == True


@pytest.mark.parametrize("check", ASN_FIXTURE_CHECKS)
def test_asn_validators_invalid(basic_validator, check, asn_fixture):
    schema = asn_fixture[check]["schema"]
    data = asn_fixture[check]["data"]["invalid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == False
