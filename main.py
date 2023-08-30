# Note:
# Example is for reference and outside of the scope of the Tech Session.
# To run you will need to create the required files. Also the example
# is not network focused but provides a reference for using additional
# files for definitions within Python.

# pip install references
import json
from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT7
from rich import print as rprint
from rich import inspect
from urllib.parse import urljoin

# Load the main schema
with open('main_schema.json') as f:
    main_schema = json.load(f)
    main_resource = DRAFT7.create_resource(main_schema)

# Extract the $id from the main schema
main_id = main_schema.get("$id", "http://example.com/schemas/main")

# Construct the IDs for the other schemas based on the main schema's URL


definition1_id = urljoin(main_id, "def1")
definition2_id = urljoin(main_id, "def2")
print(definition1_id)
print(definition2_id)

# Load other schemas (definitions)
with open('defs/def1.json') as f:
    definition1 = json.load(f)
    definition1_resource = DRAFT7.create_resource(definition1)

with open('defs/def2.json') as f:
    definition2 = json.load(f)
    definition2_resource = DRAFT7.create_resource(definition2)

# Create a registry and add the resources
registry = Registry().with_resources(
    [(main_id, main_resource),
     (definition1_id, definition1_resource),
     (definition2_id, definition2_resource)]
)

# Create a validator with the custom resolver
validator = Draft7Validator(main_schema, format_checker=FormatChecker(), registry=registry)

# Sample data to validate
host_vars = {
    "user": {
        "name": "John",
        "age": "30"
    },
    "address": {
        "street": 123,
        "city": "Anytown"
    }
}

# Validate host_vars against the main schema
errors = list(validator.iter_errors(host_vars))
if errors:
    for error in errors:
        rprint(f":cross_mark: {error.message}")
else:
    rprint(f"No validation errors found!")