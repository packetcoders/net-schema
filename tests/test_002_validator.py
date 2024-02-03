import pytest
from plugins.json_schema.validator import (  # Replace 'your_module' with the actual name of your Python file containing JSONSchemaValidator
    JSONSchemaValidator,
)

schema = {
    "type": "object",
    "properties": {"asn": {"type": "string", "format": "public"}},
    "required": ["asn"],
}

good_data = {"asn": "8000"}
bad_data = {"asn": 65000}


@pytest.fixture
def validator():
    validator = JSONSchemaValidator()
    validator.initialize(schema)
    return validator


def test_valid_data_validation(validator):
    result = validator.results(good_data)
    assert not any(error["error"] for error in result)


def test_invalid_data_validation(validator):
    result = validator.results(bad_data)
    assert any(error["error"] for error in result)
