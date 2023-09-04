import logging
import os
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="net_schema.log",
)

from jsonschema import Draft7Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT7

from helpers import load_yaml_or_json

DEFAULT_ID = "http://packetcoders.io/schemas/main"


def init_main_schema(schema_file):
    """Initialize the main schema."""
    logging.info(f"Initializing main schema from file: {schema_file}")

    main_schema = load_yaml_or_json(schema_file)

    return main_schema, DRAFT7.create_resource(main_schema)


def load_definitions(main_id, main_resource, input_def_path):
    """Load definitions from a directory."""
    logging.info("Loading definitions.")
    resources = [(main_id, main_resource)]

    def load_definitions_from_directory(directory_path):
        """Load definitions from a directory."""
        for filename in os.listdir(directory_path):
            filename_exts = (".json", ".yaml", ".yml")
            if filename.endswith(filename_exts):
                rootname, _ = os.path.splitext(filename)
                def_id = urljoin(main_id, rootname)

                definition = load_yaml_or_json(os.path.join(directory_path, filename))
                definition_resource = DRAFT7.create_resource(definition)

                resources.append((def_id, definition_resource))
                logging.debug(f"Loaded definition: {rootname} from file: {filename}")

    load_definitions_from_directory("defs")

    load_definitions_from_directory(input_def_path)

    logging.info("Definitions loaded successfully.")
    return Registry().with_resources(resources)


def init_validator(main_schema, registry):
    """Initialize the validator."""
    logging.info("Initializing JSON schema validator.")
    return Draft7Validator(
        main_schema, format_checker=FormatChecker(), registry=registry
    )


def init_json_schema_validator(schema_path, input_def_path):
    """Initialize the JSON schema validator."""
    logging.info("Initializing JSON schema validator with provided paths.")
    main_schema, main_resource = init_main_schema(schema_path)
    main_id = main_schema.get("$id", DEFAULT_ID)
    registry = load_definitions(main_id, main_resource, input_def_path)

    return init_validator(main_schema, registry)
