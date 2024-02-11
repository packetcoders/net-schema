import json

import yaml
from helpers import load_yaml_or_json


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
