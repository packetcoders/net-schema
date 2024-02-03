from pathlib import Path

import pytest
from helpers import load_yaml_or_json


@pytest.fixture
def json_file(tmp_path):
    file = tmp_path / "test.json"
    file.write_text('{"name": "test", "type": "json"}')
    return file


@pytest.fixture
def yaml_file(tmp_path):
    file = tmp_path / "test.yaml"
    file.write_text("name: test\ntype: yaml")
    return file


def test_load_json(json_file):
    """Test loading a valid JSON file"""
    result = load_yaml_or_json(json_file)
    assert result == {"name": "test", "type": "json"}


def test_load_yaml(yaml_file):
    """Test loading a valid YAML file"""
    result = load_yaml_or_json(yaml_file)
    assert result == {"name": "test", "type": "yaml"}


def test_file_not_found():
    """Test the behavior when the file does not exist"""
    with pytest.raises(SystemExit) as e:
        load_yaml_or_json(Path("nonexistent.json"))
    assert e.type == SystemExit
    assert e.value.code == 1
