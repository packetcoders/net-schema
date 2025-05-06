import json

import pytest
import yaml

from helpers import (
    DuplicateKeyError,
    SafeCustomYamlLoader,
    check_for_duplicate_keys,
    json_object_pairs_hook,
    load_yaml_or_json,
)


def test_load_yaml_file():
    """Test loading a YAML file."""
    filename = "test.yaml"
    expected_data = {"key": "value"}

    with open(filename, "w") as f:
        yaml.dump(expected_data, f)

    result = load_yaml_or_json(filename)

    assert result == expected_data


def test_load_json_file():
    """Test loading a JSON file."""
    filename = "test.json"
    expected_data = {"key": "value"}

    with open(filename, "w") as f:
        json.dump(expected_data, f)

    result = load_yaml_or_json(filename)

    assert result == expected_data


def test_invalid_input():
    """Test passing an invalid input."""
    invalid_input = 123

    try:
        load_yaml_or_json(invalid_input)
    except ValueError as e:
        assert str(e) == "Input should be a string."
    else:
        raise AssertionError()


def test_json_duplicate_keys_detected():
    """Test that a DuplicateKeyError is raised when duplicate keys are found."""
    json_data = '{"key": "value1", "key": "value2"}'
    with pytest.raises(DuplicateKeyError) as excinfo:
        json.loads(json_data, object_pairs_hook=json_object_pairs_hook)
    assert "Duplicate key found: key" in str(excinfo.value)
    assert excinfo.value.key == "key"


def test_yaml_duplicate_keys_detected():
    """Test that a DuplicateKeyError is raised when duplicate keys are found."""
    yaml_data = """
    key: value1
    key: value2
    """
    with pytest.raises(DuplicateKeyError) as excinfo:
        yaml.load(yaml_data, Loader=SafeCustomYamlLoader)  # noqa : S506
    assert "Duplicate key found: key" in str(excinfo.value)
    assert excinfo.value.key == "key"


def test_json_duplicate_keys():
    """Test that duplicate keys are detected in JSON data."""
    json_data = '{"key": "value1", "key": "value2"}'
    status, error, key = check_for_duplicate_keys(json_data, "json")
    assert not status
    assert "Duplicate key found: key" in error
    assert key == "key"


def test_json_no_duplicate_keys():
    """Test that no duplicate keys are detected in JSON data."""
    json_data = '{"key1": "value1", "key2": "value2"}'
    status, error, key = check_for_duplicate_keys(json_data, "json")
    assert status
    assert error is None
    assert key is None


def test_yaml_duplicate_keys():
    """Test that duplicate keys are detected in YAML data."""
    yaml_data = """
    key: value1
    key: value2
    """
    status, error, key = check_for_duplicate_keys(yaml_data, "yaml")
    assert not status
    assert "Duplicate key found: key" in error
    assert key == "key"


def test_yaml_no_duplicate_keys():
    """Test that no duplicate keys are detected in YAML data."""
    yaml_data = """
    key1: value1
    key2: value2
    """
    status, error, key = check_for_duplicate_keys(yaml_data, "yaml")
    assert status
