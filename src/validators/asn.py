from jsonschema.exceptions import ValidationError

ASN_MIN = 0
ASN_MAX_LEGACY = 65535
ASN_MAX = 4294967295




def asn_to_int(instance) -> int:
    """Converts an ASN in dot notation to its integer representation."""
    asn_error = f"'{instance}' is not a valid ASN."

    if "." not in instance:
        try:
            return int(instance)
        except ValueError:
            yield ValidationError(asn_error)

    asn_parts = instance.split(".")
    if len(asn_parts) != 2:
        yield ValidationError(asn_error)

    try:
        high_part, low_part = int(asn_parts[0]), int(asn_parts[1])
    except ValueError:
        yield ValidationError(asn_error)

    if not (ASN_MIN <= high_part <= ASN_MAX_LEGACY) or not (
        ASN_MIN <= low_part <= ASN_MAX_LEGACY
    ):
        yield ValidationError(asn_error)


# Custom ASN Validators
def is_public(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a public/global ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (ASN_MIN <= asn_int <= 23455 or 23457 <= asn_int <= 64495 or 131072 <= asn_int <= 4199999999):
        yield ValidationError(f"'{instance}' is not a public ASN.")


def is_private(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a private ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (64512 <= asn_int <= 65534 or 4200000000 <= asn_int <= 4294967294):
        yield ValidationError(f"'{instance}' is not a private ASN.")


def is_reserved(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a reserved ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (asn_int in {ASN_MIN, 23456, ASN_MAX_LEGACY} or 65552 <= asn_int <= 131071 or asn_int == ASN_MAX):
        yield ValidationError(f"'{instance}' is not a reserved ASN.")


def is_documentation(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a documentation ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (64496 <= asn_int <= 64511 or 65536 <= instance <= 65551):
        yield ValidationError(f"'{instance}' is not a documentation ASN.")


def is_2byte_asn(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a 2-byte ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (ASN_MIN <= asn_int <= ASN_MAX_LEGACY):
        yield ValidationError(f"'{instance}' is not a 2-byte ASN.")


def is_4byte_asn(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a 4-byte ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (ASN_MIN <= asn_int <= ASN_MAX):
        yield ValidationError(f"'{instance}' is not a 4-byte ASN.")


def is_asn(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a valid ASN, False otherwise."""
    asn_int = asn_to_int(instance)
    if not (ASN_MIN <= asn_to_int(instance) <= ASN_MAX):
        yield ValidationError(f"'{instance}' is not a valid ASN.")


def is_asn_dot_notation(validator, value, instance, schema) -> None:
    """Returns True if the ASN is a valid ASN in dot notation, False otherwise."""
    asn_int = asn_to_int(instance)
    if "." in instance and isinstance(asn_int, int):
        yield ValidationError(f"'{instance}' is not a valid ASN in dot notation.")


def is_asn_int_notation(
        validator, value, instance, schema) -> None:
    """Returns True if the ASN is a valid ASN in integer notation, False otherwise."""
    if instance == asn_to_int(instance):
        yield ValidationError(f"'{instance}' is not a valid ASN in integer notation.")


#from jsonschema import Draft7Validator
#from jsonschema.validators import extend
## Integrate custom validators to jsonschema's Draft7
#asn_validators = {
#    "public-asn": is_public,
#    "private-asn": is_private,
#    "reserved-asn": is_reserved,
#    "documentation-asn": is_documentation,
#    "2byte-asn": is_2byte_asn,
#    "4byte-asn": is_4byte_asn,
#    "asn": is_asn,
#    "asn-dot-notation": is_asn_dot_notation,
#    "asn-int-notation": is_asn_int_notation,
#}
#ASNValidator = extend(Draft7Validator, validators=asn_validators)
