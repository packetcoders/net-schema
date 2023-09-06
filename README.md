# Net Schema

## What is Net Schema
Net Schema is a library that allows you to validate the schema of your YAML documents. For example your Ansible host vars or group vars.
* Built on JSON Schema
* Provides inbuilt network-related schema definitions.
## Installing Net Schema
TBD
## Basic Usage
```
./src/main.py --document-path examples/host_vars/ --schema examples/schema.yml
❌ File: rtr001.yml Error: {'name': 'admin', 'password': 'admin'} is not of type 'integer'
❌ File: rtr001.yml Error: {'ip': '1.1.1.1'} is not of type 'integer'
❌ File: rtr001.yml Error: {'name': 'admin'} is not of type 'integer'
❌ File: rtr001.yml Error: {'id': 1} is not of type 'string'
❌ File: rtr004.yml Error: 'asn' is a required property
❌ File: rtr004.yml Error: 'vlan' is a required property
❌ File: rtr003.yml Error: 'asn' is a required property
❌ File: rtr003.yml Error: 'vlan' is a required property
❌ File: rtr002.yml Error: 'asn' is a required property
❌ File: rtr002.yml Error: 'vlan' is a required property
❌ File: rtr005.yml Error: 'asn' is a required property
❌ File: rtr005.yml Error: 'vlan' is a required property
```

## Builtin Definitions
Net Schema provides various inbuilt schema definitions. Allowing you to use these definitions to validate things such as VLAN data and ASN data rather then having to define you own schema.

### `asn`
* Usage:
```
"$ref": "asn#/definitions/asn"
```
* Schema:
```
TBC
```

### `vlan`
* Usage:
```
"$ref": "vlan#/definitions/vlan"
```
* Schema:
```
TBC
```
## Custom Definitions
Custom definitions can also be supplied using the `--def-path` option. Custom defintions can be supplied as either YAML or JSON.


