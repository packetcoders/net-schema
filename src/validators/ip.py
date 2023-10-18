import ipaddress


def is_multicast(instance) -> bool:
    """Check if the IP address is a multicast address."""
    try:
        return ipaddress.ip_address(instance).is_multicast
    except ValueError:
        return False


def is_private(instance) -> bool:
    """Check if the IP address is a private address."""
    try:
        return ipaddress.ip_address(instance).is_private
    except ValueError:
        return False


def is_unspecified(instance) -> bool:
    """Check if the IP address is an unspecified address."""
    try:
        return ipaddress.ip_address(instance).is_unspecified
    except ValueError:
        return False


def is_reserved(instance) -> bool:
    """Check if the IP address is a reserved address."""
    try:
        return ipaddress.ip_address(instance).is_reserved
    except ValueError:
        return False


def is_loopback(instance) -> bool:
    """Check if the IP address is a loopback address."""
    try:
        return ipaddress.ip_address(instance).is_loopback
    except ValueError:
        return False


def is_link_local(instance) -> bool:
    """Check if the IP address is a link-local address."""
    try:
        return ipaddress.ip_address(instance).is_link_local
    except ValueError:
        return False


def is_ipv4(instance) -> bool:
    """Check if the IP address is an IPv4 address."""
    try:
        return isinstance(ipaddress.ip_address(instance), ipaddress.IPv4Address)
    except ValueError:
        return False


def is_ipv6(instance) -> bool:
    """Check if the IP address is an IPv6 address."""
    try:
        return isinstance(ipaddress.ip_address(instance), ipaddress.IPv6Address)
    except ValueError:
        return False


def is_ipaddress(instance) -> bool:
    """Check if the IP address is an IP address."""
    try:
        ipaddress.ip_address(instance)
        return True
    except ValueError:
        return False


def is_network(instance) -> bool:
    """Check if the IP address is a network."""
    try:
        ipaddress.ip_network(instance, strict=False)
        return True
    except ValueError:
        return False


def is_ip_interface(instance) -> bool:
    """Check if the IP address is an IP interface."""
    try:
        ipaddress.ip_interface(instance)
        return True
    except ValueError:
        return False


def is_shared(instance) -> bool:
    """Check if the IP address is a shared address."""
    try:
        return ipaddress.ip_address(instance) in ipaddress.ip_network("100.64.0.0/10")
    except ValueError:
        return False


def is_documentation(instance) -> bool:
    """Check if the IP address is a documentation address."""
    try:
        return (
            ipaddress.ip_address(instance).is_reserved
            and not ipaddress.ip_address(instance).is_private
            and not is_shared(instance)
        )
    except ValueError:
        return False
