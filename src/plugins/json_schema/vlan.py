from collections.abc import Generator
from jsonschema.exceptions import ValidationError


def vlan(validator, value, instance, schema) -> Generator:
    """Check if the value is a valid VLAN ID."""
    try:
        vlan_id = int(instance)
        if not (1 <= vlan_id <= 4094):
            yield ValidationError(
                f"'{instance}' is not a valid VLAN ID. It must be between 1 and 4094."
            )
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid VLAN ID. It must be an integer.")


def vlan_standard(validator, value, instance, schema) -> Generator:
    """Check if the value is a standard VLAN ID (1-1001)."""
    try:
        vlan_id = int(instance)

        if not (1 <= vlan_id <= 1001):
            yield ValidationError(
                f"'{instance}' is not a standard VLAN ID. It must be between 1 and 1001."
            )
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid VLAN ID. It must be an integer.")


def vlan_extended(validator, value, instance, schema) -> Generator:
    """Check if the value is an extended VLAN ID (1006-4094)."""
    try:
        vlan_id = int(instance)
        if not (1006 <= vlan_id <= 4094):
            yield ValidationError(
                f"'{instance}' is not an extended VLAN ID. It must be between 1006 and 4094."
            )
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid VLAN ID. It must be an integer.")
