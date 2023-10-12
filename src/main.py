def main(document_path="examples/host_vars",
         schema_path="examples/schema.json",
         def_path="examples/defs"):
    """
    Validates YAML files in the document_path directory against the JSON schema.
    """
    logging.debug("✅ Starting validation process.")

    # Get absolute path of the directory containing the script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert relative paths to absolute paths
    abs_document_path = os.path.join(base_dir, document_path)
    abs_schema_path = os.path.join(base_dir, schema_path)
    abs_def_path = os.path.join(base_dir, def_path)
    print(abs_schema_path)
    # Load schema and definitions from files
    main_schema = load_yaml_or_json(abs_schema_path)
    definitions = {}
    for filename in os.listdir(abs_def_path):
        if filename.endswith(('.yaml', '.yml', '.json')):
            rootname = os.path.splitext(filename)[0]
            definitions[rootname] = load_yaml_or_json(os.path.join(abs_def_path, filename))

    # Create validator
    validator = JSONSchemaValidator(main_schema, definitions)
    errors = []

    for filename in os.listdir(abs_document_path):
        if filename.endswith(('.yaml', '.yml')):
            host_vars_data = load_yaml_or_json(os.path.join(abs_document_path, filename))

            file_errors = validator.errors(host_vars_data)

            if file_errors:
                for error in file_errors:
                    logging.error(f"Error in file {filename}: {error['error']}")
                    rprint(f":cross_mark: File: {filename} Error: {error['error']}")
                errors.extend(file_errors)
            else:
                logging.info(f"File {filename} validated successfully.")
                rprint(f"File: {filename} - No validation errors found!")

    if errors:
        sys.exit(1)
