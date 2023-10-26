import jsonschema
from jsonschema import Draft7Validator, exceptions
from jsonschema.validators import extend

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


@pytest.fixture(scope="session")
def basic_validator():
    def _basic_validator(schema):
        v = Draft7Validator(schema=schema, format_checker=FormatChecker())
        Draft7Validator.VALIDATORS.update(VALIDATORS)
        return v

    return _basic_validator


# Test for is_public
def test_asn_public_valid():
    """Test for asn_public with valid data."""
    schema = {"type": "string", "format": "public-asn"}
    data = "8000"  # or any other valid public ASN
    jsonschema.validate(data, schema, format_checker=jsonschema.draft7_format_checker)


def test_asn_public_invalid():
    """Test for asn_public with invalid data."""
    schema = {"type": "string", "format": "public-asn"}
    data = "65000"  # or any other invalid public ASN
    with pytest.raises(exceptions.ValidationError):
        jsonschema.validate(
            data, schema, format_checker=jsonschema.draft7_format_checker
        )




# Test for is_private
def test_asn_private_valid():
    """Test for asn_public with valid data."""
    schema = {"type": "string", "format": "private-asn"}
    data = "65000"  # or any other valid private ASN
    jsonschema.validate(data, schema, format_checker=jsonschema.draft7_format_checker)


def test_asn_private_invalid():
    """Test for asn_public with invalid data."""
    schema = {"type": "string", "format": "private-asn"}
    data = "8000"  # or any other invalid private ASN
    with pytest.raises(exceptions.ValidationError):
        jsonschema.validate(
            data, schema, format_checker=jsonschema.draft7_format_checker
        )
