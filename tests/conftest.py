import sys
from pathlib import Path

import pytest

sys.path.append(f"{Path(__file__).parent.parent}/src")
from pathlib import Path

from net_schema import (
    init_json_schema_validator,
    init_main_schema,
    init_validator,
    load_definitions,
)

BASE_SCHEMA = "tests/fixtures/schema.json"
BASE_DEFS_PATH = "tests/fixtures/defs/"
DEFAULT_ID = "http://packetcoders.io/schemas/main"
CUSTOM_DEFS_PATH = "tests/fixtures/defs/"


@pytest.fixture
def main_schema_and_resource():
    return init_main_schema(BASE_SCHEMA)


@pytest.fixture
def definitions(main_schema_and_resource):
    main_schema, main_resource = main_schema_and_resource
    main_id = main_schema.get("$id", DEFAULT_ID)
    return load_definitions(main_id, main_resource, CUSTOM_DEFS_PATH)


@pytest.fixture
def validator(main_schema_and_resource, definitions):
    return init_validator(main_schema_and_resource[0], definitions)


@pytest.fixture
def json_schema_validator():
    return init_json_schema_validator(BASE_SCHEMA, CUSTOM_DEFS_PATH)
