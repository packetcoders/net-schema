"""Module contains tests for the JSONSchemaValidator class."""

import pytest
from plugins.json_schema.validator import JSONSchemaValidator

schema = {
    "type": "object",
    "properties": {"asn": {"type": "string", "format": "public"}},
    "required": ["asn"],
}

good_data = {"asn": "8000"}
bad_data = {"asn": 65000}


@pytest.fixture
def validator():
    """Return a JSONSchemaValidator instance."""
    """Return a JSONSchemaValidator instance."""
    validator = JSONSchemaValidator()
    validator.initialize(schema)
    return validator


def test_valid_data_validation(validator):
    """Test valid data."""
    result = validator.results(good_data)
    assert not any(error["error"] for error in result)


def test_invalid_data_validation(validator):
    """Test invalid data."""
    result = validator.results(bad_data)
    assert any(error["error"] for error in result)
