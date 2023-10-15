#!/usr/bin/env python3
import jsonschema
from jsonschema import Draft7Validator, exceptions
from netutils.asn import asn_to_int


def normalize_asn(asn) -> int:
    """Returns the ASN as an integer if it is a valid ASN, False otherwise."""
    try:
        return int(asn_to_int(asn))
    except ValueError:
        return False


# Custom ASN Validators
def is_global(asn) -> int:
    """Returns True if the ASN is a public/global ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return (
        (
            1 <= asn_int <= 23455
            or 23457 <= asn_int <= 64495
            or 131072 <= asn_int <= 4199999999
        )
        if isinstance(asn_int, int)
        else asn_int
    )


def is_private(asn) -> int:
    """Returns True if the ASN is a private ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return (
        (64512 <= asn_int <= 65534 or 4200000000 <= asn_int <= 4294967294)
        if isinstance(asn_int, int)
        else asn_int
    )


def is_reserved(asn) -> int:
    """Returns True if the ASN is a reserved ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return (
        (
            asn_int in {0, 23456, 65535}
            or 65552 <= asn_int <= 131071
            or asn_int == 4294967295
        )
        if isinstance(asn_int, int)
        else asn_int
    )


def is_documentation(asn) -> int:
    """Returns True if the ASN is a documentation ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return (
        (64496 <= asn_int <= 64511 or 65536 <= asn <= 65551)
        if isinstance(asn_int, int)
        else asn_int
    )


def is_2byte_asn(asn) -> int:
    """Returns True if the ASN is a 2-byte ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return 1 <= asn_int <= 65535 if isinstance(asn_int, int) else asn_int


def is_4byte_asn(asn) -> int:
    """Returns True if the ASN is a 4-byte ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return 1 <= asn_int <= 4294967295 if isinstance(asn_int, int) else asn_int


def is_asn(asn) -> bool:
    """Returns True if the ASN is a valid ASN, False otherwise."""
    asn_int = normalize_asn(asn)
    return (
        1 <= normalize_asn(asn_int) <= 4294967295
        if isinstance(asn_int, int)
        else asn_int
    )


def is_asn_dot_notation(asn) -> bool:
    """Returns True if the ASN is a valid ASN in dot notation, False otherwise."""
    return ":" in asn


def is_asn_int_notation(asn) -> bool:
    """Returns True if the ASN is a valid ASN in integer notation, False otherwise."""
    return asn == normalize_asn(asn)


# Add custom validators to jsonschema's Draft7
Draft7Validator.VALIDATORS.update(
    {"format": Draft7Validator.VALIDATORS["format"].copy()}
)
Draft7Validator.VALIDATORS["format"].update(
    {
        "global-asn": is_global,
        "private-asn": is_private,
        "reserved-asn": is_reserved,
        "documentation-asn": is_documentation,
        "2byte-asn": is_2byte_asn,
        "4byte-asn": is_4byte_asn,
        "asn": is_asn,
        "asn-dot-notation": is_asn_dot_notation,
        "asn-int-notation": is_asn_int_notation,
    }
)

# Example schema using the new ASN formats
schema = {
    "type": "object",
    "properties": {
        "global_asn": {"type": "integer", "format": "global-asn"},
        "private_asn": {"type": "integer", "format": "private-asn"},
        # ... Similarly for other ASNs
    },
    "required": ["global_asn", "private_asn"],
}

# Example ASN data
data = {
    "global_asn": 131072,
    "private_asn": 64512,
    # ... Similarly for other ASNs
}

# Validate the data against the schema
try:
    jsonschema.validate(data, schema, format_checker=jsonschema.draft7_format_checker)
    print("Validation successful!")
except exceptions.ValidationError as e:
    print(f"Validation failed: {e.message}")