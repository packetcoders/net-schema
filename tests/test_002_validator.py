"""Module contains tests for the JSONSchemaValidator class."""

import pytest

from plugins.json_schema.validator import JSONSchemaValidator


@pytest.fixture
def schema():
    """Return a schema for testing."""
    return {
        "type": "object",
        "properties": {"asn": {"type": "string", "format": "public"}},
        "required": ["asn"],
    }


@pytest.fixture
def good_data():
    """Return data that matches the schema."""
    return {"asn": "8000"}


@pytest.fixture
def bad_data():
    """Return data that does not match the schema."""
    return {"asn": 65000}


@pytest.fixture
def validator(schema):
    """Return a JSONSchemaValidator instance."""
    validator = JSONSchemaValidator()
    validator.initialize(schema)
    return validator


def test_valid_data_validation(validator, good_data):
    """Test valid data."""
    result = validator.results(good_data)
    assert not any(error["error"] for error in result)


def test_invalid_data_validation(validator, bad_data):
    """Test invalid data."""
    result = validator.results(bad_data)
    assert any(error["error"] for error in result)
