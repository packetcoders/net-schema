from helpers import load_yaml_or_json


def test_load_yaml():
    """
    Test if the YAML file is loaded successfully.
    """
    yaml_file = load_yaml_or_json("tests/fixtures/schema.yml")

    assert isinstance(yaml_file, dict), "YAML file should be a dictionary"
    assert "$id" in yaml_file, "YAML file should have '$id' key"
    assert "properties" in yaml_file, "YAML file should have 'properties' key"


def test_load_json():
    """
    Test if the JSON file is loaded successfully.
    """
    json_file = load_yaml_or_json("tests/fixtures/schema.yml")

    assert isinstance(json_file, dict), "JSON file should be a dictionary"
    assert "$id" in json_file, "JSON file should have '$id' key"
    assert "properties" in json_file, "JSON file should have 'properties' key"
