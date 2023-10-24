import ipaddress

from jsonschema.exceptions import ValidationError


def ip_multicast(validator, value, instance, schema) -> None:
    """Check if the IP address is a multicast address."""
    try:
        if not ipaddress.ip_address(instance).is_multicast:
            yield ValidationError(f"'{instance}' is not a multicast IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_private(validator, value, instance, schema) -> None:
    """Check if the IP address is a private address."""
    try:
        if not ipaddress.ip_address(instance).is_private:
            yield ValidationError(f"'{instance}' is not a private IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def is_unspecified(validator, value, instance, schema) -> None:
    """Check if the IP address is an unspecified address."""
    try:
        if not ipaddress.ip_address(instance).is_unspecified:
            yield ValidationError(f"'{instance}' is not an unspecified IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_reserved(validator, value, instance, schema) -> None:
    """Check if the IP address is a reserved address."""
    try:
        if not ipaddress.ip_address(instance).is_reserved:
            yield ValidationError(f"'{instance}' is not a reserved IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_loopback(validator, value, instance, schema) -> None:
    """Check if the IP address is a loopback address."""
    try:
        if not ipaddress.ip_address(instance).is_loopback:
            yield ValidationError(f"'{instance}' is not a loopback IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_linklocal(validator, value, instance, schema) -> None:
    """Check if the IP address is a link-local address."""
    try:
        if not ipaddress.ip_address(instance).is_link_local:
            yield ValidationError(f"'{instance}' is not a link-local IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_ipv4(validator, value, instance, schema) -> None:
    """Check if the IP address is an IPv4 address."""
    try:
        if not isinstance(ipaddress.ip_address(instance), ipaddress.IPv4Address):
            yield ValidationError(f"'{instance}' is not an IPv4 address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_ipv6(validator, value, instance, schema) -> None:
    """Check if the IP address is an IPv6 address."""
    try:
        if not isinstance(ipaddress.ip_address(instance), ipaddress.IPv6Address):
            yield ValidationError(f"'{instance}' is not an IPv6 address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_ipaddress(validator, value, instance, schema) -> None:
    """Check if the IP address is an IP address."""
    try:
        ipaddress.ip_address(instance)
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def ip_network(validator, value, instance, schema) -> None:
    """Check if the IP address is a network."""
    try:
        ipaddress.ip_network(instance, strict=False)
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP network.")


def ip_interface(validator, value, instance, schema) -> None:
    """Check if the IP address is an IP interface."""
    try:
        ipaddress.ip_interface(instance)
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP interface.")


def ip_shared(validator, value, instance, schema) -> None:
    """Check if the IP address is a shared address."""
    try:
        if instance not in ipaddress.ip_network("100.64.0.0/10"):
            yield ValidationError(f"'{instance}' is not a shared IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")


def is_documentation(validator, value, instance, schema) -> None:
    """Check if the IP address is a documentation address."""
    try:
        ip = ipaddress.ip_address(instance)
        if not (
            ip.is_reserved
            and not ip.is_private
            and instance not in ipaddress.ip_network("100.64.0.0/10")
        ):
            yield ValidationError(f"'{instance}' is not a documentation IP address.")
    except ValueError:
        yield ValidationError(f"'{instance}' is not a valid IP address.")
