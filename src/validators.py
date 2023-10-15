def asn_to_int(asn):
    """Converts an ASN in dot notation to its integer representation."""
    if ":" in asn:
        x, y = map(int, asn.split(":"))
        return x * (2 ** 16) + y
    else:
        return int(asn)


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
