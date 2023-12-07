import json
import sys
from pathlib import Path

import pytest

sys.path.append(f"{Path(__file__).parent.parent}/src")


ASN_FIXTURE = f"{Path(__file__).parent}/fixtures/asn.json"
ASN_FIXTURE_CHECKS = [
    "asn_min",
    "asn_max",
    "asn_public_min",
    "asn_public_max",
    "asn_private_min",
    "asn_private_max",
    "asn_reserved_min",
    "asn_reserved_max",
    "asn_documentation_min",
    "asn_documentation_max",
    "asn_2byte_min",
    "asn_2byte_max",
    "asn_4byte_min",
    "asn_4byte_max",
]


@pytest.fixture(scope="session")
def asn_fixture():
    with open(ASN_FIXTURE) as file:
        data = json.load(file)
    return data


@pytest.mark.parametrize("check", ASN_FIXTURE_CHECKS)
def test_asn_validators_valid(basic_validator, check, asn_fixture):
    schema = asn_fixture[check]["schema"]
    data = asn_fixture[check]["data"]["valid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == True


@pytest.mark.parametrize("check", ASN_FIXTURE_CHECKS)
def test_asn_validators_invalid(basic_validator, check, asn_fixture):
    schema = asn_fixture[check]["schema"]
    data = asn_fixture[check]["data"]["invalid"]

    v = basic_validator(schema)
    assert v.is_valid(data) == False
