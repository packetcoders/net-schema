import pathlib
import sys

from jsonschema import Draft7Validator

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

import pytest
from jsonschema import (
    Draft7Validator,
    FormatChecker,
)

from src.plugins.json_schema.asn import (
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


@pytest.fixture(scope="session")
def basic_validator():
    def _basic_validator(schema):
        v = Draft7Validator(schema=schema, format_checker=FormatChecker())
        Draft7Validator.VALIDATORS.update(VALIDATORS)
        return v

    return _basic_validator


def test_asn_valid(basic_validator):
    schema = {
        "properties": {"asn": {"type": "integer", "asn": True}},
    }
    data = {"asn": 1000}

    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_public_valid(basic_validator):
    schema = {
        "properties": {"asn_public": {"type": "string", "asn_public": True}},
    }
    data = {"asn_public": "valid_data_for_public_asn"}  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_private_valid(basic_validator):
    schema = {
        "properties": {"asn_private": {"type": "string", "asn_private": True}},
    }
    data = {
        "asn_private": "valid_data_for_private_asn"
    }  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data)


def test_asn_reserved_valid(basic_validator):
    schema = {
        "properties": {"asn_reserved": {"type": "string", "asn_reserved": True}},
    }
    data = {
        "asn_reserved": "valid_data_for_reserved_asn"
    }  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_documentation_valid(basic_validator):
    schema = {
        "properties": {
            "asn_documentation": {"type": "string", "asn_documentation": True}
        },
    }
    data = {
        "asn_documentation": "valid_data_for_documentation_asn"
    }  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_2byte_valid(basic_validator):
    schema = {
        "properties": {"asn_2byte": {"type": "string", "asn_2byte": True}},
    }
    data = {"asn_2byte": "valid_data_for_2byte_asn"}  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_4byte_valid(basic_validator):
    schema = {
        "properties": {"asn_4byte": {"type": "string", "asn_4byte": True}},
    }
    data = {"asn_4byte": "valid_data_for_4byte_asn"}  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_asn_valid(basic_validator):
    schema = {
        "properties": {"asn_asn": {"type": "string", "asn_asn": True}},
    }
    data = {"asn_asn": "valid_data_for_asn"}  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_dot_notation_valid(basic_validator):
    schema = {
        "properties": {
            "asn_dot-notation": {"type": "string", "asn_dot-notation": True}
        },
    }
    data = {
        "asn_dot-notation": "valid_data_for_dot_notation"
    }  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None


def test_asn_int_notation_valid(basic_validator):
    schema = {
        "properties": {
            "asn_int-notation": {"type": "string", "asn_int-notation": True}
        },
    }
    data = {
        "asn_int-notation": "valid_data_for_int_notation"
    }  # Replace with actual valid data
    v = basic_validator(schema=schema)
    assert v.validate(instance=data) == None
