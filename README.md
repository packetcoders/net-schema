# Net Schema

## About this Project

Net Schema is a library that validates JSON and YAML documents against a defined schema, utilizing JSON Schema. This ensures that data adheres to specified formats and rules.

Additionally, this project is designed for schema validation of network-specific data, providing a range of network-related custom validators.

## Installation

To install the Net Schema library, perform the following:

**Pip**

```bash
pip install net-schema
```

**Poetry**

```bash
poetry add net-schema
```

## Usage
Net Schema provides a CLI. You pass in the path to your documents, along with your schema path. Then Net Schema validates your data against the schema.

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

> [!NOTE]
> Net Schema also provides an additional option to check for the presence of duplicate keys within your YAML or JSON data via the `--check-dup-keys` option.

## Custom Validators

Net Schema provides various custom validators that can be used within your schema.

### Usage

To utilize custom validators within your schema, provide the name of the validator as a **key**, and then provide `True` as its value.

Below provides an example of using the `ip` custom validator to ensure the `dns_server` value is of an IP address format.
```
---
type: object
properties:
  dns_server:
    ip: True
```

### ASN Validators

| Validator Name         | Checks                                                      |
|------------------------|-------------------------------------------------------------|
| `asn`                  | Validates whether the ASN is valid in general.              |
| `asn_public`           | Checks if the ASN is a public/global ASN.                   |
| `asn_private`          | Determines if the ASN is a private ASN.                     |
| `asn_reserved`         | Identifies if the ASN is reserved.                          |
| `asn_documentation`    | Validates if the ASN is meant for documentation.            |
| `asn_2byte`            | Checks if the ASN falls within the 2-byte ASN range.        |
| `asn_4byte`            | Checks if the ASN falls within the 4-byte ASN range.        |
| `asn_notation_dot`     | Validates ASN format in dot notation.                       |
| `asn_notation_int`     | Validates ASN format in integer notation.

### IP Validators

| Validator Name   | Checks                                                         |
|------------------|----------------------------------------------------------------|
| `ip`             | Validates if the instance is a valid IP address.               |
| `ip_ipv4`        | Checks if the instance is a valid IPv4 address.                |
| `ip_ipv6`        | Checks if the instance is a valid IPv6 address.                |
| `ip_multicast`   | Determines if the instance is a multicast IP address.          |
| `ip_private`     | Validates if the instance is a private IP address.             |
| `ip_reserved`    | Identifies if the instance is a reserved IP address.           |
| `ip_linklocal`   | Checks if the instance is a link-local IP address.             |
| `ip_network`     | Validates if the instance represents a valid IP network.       |

### VLAN Validators

| Validator Name    | Checks                                                                       |
|-------------------|------------------------------------------------------------------------------|
| `vlan`            | Validates if the instance is a valid VLAN ID (between 1 and 4094).           |
| `vlan_standard`   | Checks if the instance is a standard VLAN ID (between 1 and 1001).           |
| `vlan_extended`   | Determines if the instance is an extended VLAN ID (between 1006 and 4094).   |




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