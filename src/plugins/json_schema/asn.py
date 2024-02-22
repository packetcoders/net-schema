from typing import Generator

from jsonschema.exceptions import ValidationError

ASN_MIN = 0
ASN_MAX_LEGACY = 65535
ASN_MAX = 4294967295


def asn_to_int(instance) -> int:
    """Converts an ASN in dot notation to its integer representation."""
    asn_error = f"'{instance}' is not a valid ASN."

    if not isinstance(instance, (int, str)) or isinstance(instance, bool):
        raise ValidationError(asn_error)

    if isinstance(instance, str) and "." not in instance:
        try:
            return int(instance)
        except ValueError:
            raise ValidationError(asn_error)

    asn_parts = instance.split(".")

    if len(asn_parts) != 2:
        raise ValidationError(asn_error)

    try:
        high_part, low_part = int(asn_parts[0]), int(asn_parts[1])
    except ValueError:
        raise ValidationError(asn_error)

    if not (ASN_MIN <= high_part <= ASN_MAX_LEGACY) or not (
        ASN_MIN <= low_part <= ASN_MAX_LEGACY
    ):
        raise ValidationError(asn_error)

    return int(instance)


# Custom ASN Validators
def asn(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a valid ASN, False otherwise."""
    # Check if instance is a string given schema type excepts a string.
    if not isinstance(instance, str):
        pass
    else:
        try:
            asn_int = asn_to_int(instance)

            if not (ASN_MIN <= asn_int <= ASN_MAX):
                yield ValidationError(f"'{instance}' is not a valid ASN.")

        except ValidationError as e:
            yield e


def asn_public(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a public/global ASN, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if not (
            ASN_MIN <= asn_int <= 23455
            or 23457 <= asn_int <= 64495
            or 131072 <= asn_int <= 4199999999
        ):
            yield ValidationError(f"'{instance}' is not a public ASN.")
    except ValidationError as e:
        yield e


def asn_private(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a private ASN, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if not (64512 <= asn_int <= 65534 or 4200000000 <= asn_int <= 4294967294):
            yield ValidationError(f"'{instance}' is not a private ASN.")
    except ValidationError as e:
        yield e


def asn_reserved(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a reserved ASN, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if not (
            asn_int in {ASN_MIN, 23456, ASN_MAX_LEGACY}
            or 65552 <= asn_int <= 131071
            or asn_int == ASN_MAX
        ):
            yield ValidationError(f"'{instance}' is not a reserved ASN.")
    except ValidationError as e:
        yield e


def asn_documentation(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a documentation ASN, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if not (64496 <= asn_int <= 64511 or 65536 <= asn_int <= 65551):
            yield ValidationError(f"'{instance}' is not a documentation ASN.")
    except ValidationError as e:
        yield e


def asn_2byte(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a 2-byte ASN, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if not (ASN_MIN <= asn_int <= ASN_MAX_LEGACY):
            yield ValidationError(f"'{instance}' is not a 2-byte ASN.")
    except ValidationError as e:
        yield e


def asn_4byte(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a 4-byte ASN, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if not (ASN_MIN <= asn_int <= ASN_MAX):
            yield ValidationError(f"'{instance}' is not a 4-byte ASN.")
    except ValidationError as e:
        yield e


def asn_notation_dot(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a valid ASN in dot notation, False otherwise."""
    try:
        asn_int = asn_to_int(instance)
        if "." in instance and isinstance(asn_int, int):
            yield ValidationError(f"'{instance}' is not a valid ASN in dot notation.")
    except ValidationError as e:
        yield e


def asn_notation_int(validator, value, instance, schema) -> Generator:
    """Returns True if the ASN is a valid ASN in integer notation, False otherwise."""
    try:
        if instance == asn_to_int(instance):
            yield ValidationError(f"'{instance}' is not a valid ASN in integer notation.")
    except ValidationError as e:
        yield e
