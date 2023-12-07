import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, FormatChecker

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
    # Load your fixture data from the JSON file
    with open(IP_FIXTURE) as file:
        data = json.load(file)
    return data


@pytest.mark.parametrize("check", IP_FIXTURE_CHECKS)
def test_ip_validators_valid(basic_validator, check, ip_fixture):
    schema = ip_fixture[check]["schema"]
    data = ip_fixture[check]["data"]["valid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == True


@pytest.mark.parametrize("check", IP_FIXTURE_CHECKS)
def test_ip_validators_invalid(basic_validator, check, ip_fixture):
    schema = ip_fixture[check]["schema"]
    data = ip_fixture[check]["data"]["invalid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == False
