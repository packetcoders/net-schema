# Net Schema

## About this Project

Net Schema is a library that allows you to schema validate your JSON and YAML documents, based upon a schema.
The current schema support is JSON Schema.

## Installation

To install the Net Schema library, you can use the following command:

**Pip**
```bash
pip install net-schema
```

**Poetry**
```bash
poetry add net-schema
```

## Usage
Net Schema provides a CLI. You pass in the path to your documents, along with your schema path. From which Net Schema then validates your data.

```bash
net-schema --help
Usage: net-schema [OPTIONS]

  Validate a directory of YAML and JSON files against a schema.

Options:
  -p, --document_path PATH  Path to the documents directory  [required]
  -s, --schema PATH         Path to the schema file  [required]
  -k, --check-dup-keys      Check for duplicate keys in JSON or YAML documents
  --help                    Show this message and exit.
```

> Note:
> Net Schema also provides an additional option to check for the presense of duplicate keys within your YAML or JSON data.

## Example

```bash
❯ net-schema --document_path examples/host_vars/ --schema examples/schema.yaml --check-dup-keys
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Result   Filename                         Key       Msg
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ❌       examples/host_vars/rtr001.yml    asn       Duplicate key found: asn
  ❌       examples/host_vars/rtr001.yml    asn       '4294967297' is not a valid ASN.
  ❌       examples/host_vars/rtr001.yml    bad_asn   {'name': 'admin', 'password': 'admin'} is not of type 'string'
  ✅       examples/host_vars/rtr002.yml    --        --
  ✅       examples/host_vars/rtr003.yml    --        --
  ✅       examples/host_vars/rtr004.yml    --        --
  ❌       examples/host_vars/rtr005.json   asn       Duplicate key found: asn
  ❌       examples/host_vars/rtr005.json   asn       '4294967298' is not a valid ASN.
  ❌       examples/host_vars/rtr005.json   bad_asn   {'name': 'admin', 'password': 'admin'} is not of type 'string'
  ✅       examples/host_vars/rtr005.yml    --        --
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

## License
TBC