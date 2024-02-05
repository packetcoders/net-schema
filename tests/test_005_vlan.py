"""Test the VLAN validators."""

import json
import sys
from pathlib import Path

import pytest

sys.path.append(f"{Path(__file__).parent.parent}/src")


VLAN_FIXTURE = f"{Path(__file__).parent}/fixtures/vlan.json"

VLAN_FIXTURE_CHECKS = ["vlan_valid", "vlan_standard_valid", "vlan_extended_valid"]


@pytest.fixture(scope="session")
def vlan_fixture():
    """
    Fixture that loads VLAN data from a JSON file.

    Returns
    -------
        dict: The loaded VLAN data.
    """
    with open(VLAN_FIXTURE) as file:
        return json.load(file)


@pytest.mark.parametrize("check", VLAN_FIXTURE_CHECKS)
def test_vlan_validators_valid(basic_validator, check, vlan_fixture):
    """
    Test the validity of VLAN validators.

    Args:
        basic_validator: The basic validator object.
        check: The check parameter for the test.
        vlan_fixture: The VLAN fixture data.

    Returns
    -------
        None
    """
    schema = vlan_fixture[check]["schema"]
    data = vlan_fixture[check]["data"]["valid"]
    v = basic_validator(schema)
    assert v.is_valid(data) == True


@pytest.mark.parametrize("check", VLAN_FIXTURE_CHECKS)
def test_vlan_validators_invalid(basic_validator, check, vlan_fixture):
    """
    Test invalid VLAN data.

    Args:
        basic_validator: The basic validator object.
        check: The check parameter for the test.
        vlan_fixture: The VLAN fixture data.

    Returns
    -------
        None
    """
    schema = vlan_fixture[check]["schema"]
    data = vlan_fixture[check]["data"]["invalid"]
    v = basic_validator(schema)
    assert v.is_valid(data) == False
