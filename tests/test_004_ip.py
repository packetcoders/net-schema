"""Test cases for IP address validators."""

import json
import sys
from pathlib import Path

import pytest

sys.path.append(f"{Path(__file__).parent.parent}/src")


IP_FIXTURE = f"{Path(__file__).parent}/fixtures/ip.json"

IP_FIXTURE_CHECKS = [
    "ip_valid",
    "ipv4_valid",
    "ipv6_valid",
    "ip_multicast_valid",
    "ip_private_valid",
    "ip_reserved_valid",
    "ip_linklocal_valid",
]


@pytest.fixture(scope="session")
def ip_fixture():
    """Fixture that loads data from IP_FIXTURE file and returns it."""
    with open(IP_FIXTURE) as file:
        data = json.load(file)
    return data


@pytest.mark.parametrize("check", IP_FIXTURE_CHECKS)
def test_ip_validators_valid(basic_validator, check, ip_fixture):
    """
    Test the validity of IP validators.

    Args:
        basic_validator: The basic validator object.
        check: The check parameter for the test.
        ip_fixture: The IP fixture data.

    Returns
    -------
        None
    """
    schema = ip_fixture[check]["schema"]
    data = ip_fixture[check]["data"]["valid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == True


@pytest.mark.parametrize("check", IP_FIXTURE_CHECKS)
def test_ip_validators_invalid(basic_validator, check, ip_fixture):
    """
    Test case for validating invalid IP addresses using basic_validator.

    Args:
        basic_validator: The basic_validator object.
        check: The check parameter from IP_FIXTURE_CHECKS.
        ip_fixture: The IP fixture containing the schema and data.

    Returns
    -------
        None
    """
    schema = ip_fixture[check]["schema"]
    data = ip_fixture[check]["data"]["invalid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == False
