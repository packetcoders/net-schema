from jsonschema import Draft7Validator
from main import (
    # init_json_schema_validator,
    # init_main_schema,
    # init_validator,
    load_definitions,
)

# Assuming these paths are correct, please adjust as necessary
schema_path = "tests/fixtures/schema.json"
custom_def_path = "tests/fixtures/defs/custom/"


# def test_init_main_schema():
#    """
#    Test if the initialization of the main schema is successful and contains expected keys.
#    """
#    main_schema, resource = init_main_schema(schema_path)
#
#    assert isinstance(main_schema, dict), "Main schema should be a dictionary"
#    assert "$id" in main_schema, "Main schema should have '$id' key"
#    assert "properties" in main_schema, "Main schema should have 'properties' key"
#    assert resource is not None, "Resource initialization failed - Resource is None"


def test_load_definitions():
    """
    Test if the definitions are loaded successfully.
    """
    main_schema, main_resource = init_main_schema(schema_path)
    main_id = main_schema.get("$id", "http://packetcoders.io/schemas/main")
    registry = load_definitions(main_id, main_resource, custom_def_path)

    assert registry is not None, "Registry should not be None"
    assert (
        len(registry._resources) == 5
    ), "Registry should contain more than one resource"


# def test_init_validator():
#    """
#    Test if the validator is initialized successfully.
#    """
#    main_schema, main_resource = init_main_schema(schema_path)
#    main_id = main_schema.get("$id", "http://packetcoders.io/schemas/main")
#    registry = load_definitions(main_id, main_resource, custom_def_path)
#
#    validator = init_validator(main_schema, registry)
#
#    assert validator is not None, "Validator should not be None"
#    assert isinstance(
#        validator, Draft7Validator
#    ), "Validator should be an instance of Draft7Validator"


# def test_init_json_schema_validator():
#    """
#    Test if the JSON schema validator is initialized successfully.
#    """
#    validator = init_json_schema_validator(schema_path, custom_def_path)
#
#    assert validator is not None, "JSON Schema Validator should not be None"
#    assert isinstance(
#        validator, Draft7Validator
#    ), "JSON Schema Validator should be an instance of Draft7Validator"


# def test_validation_results():
#    """
#    Test if the validation results are as expected (this needs to be implemented).
#    """
#    pass  # TODO: Implement this test
