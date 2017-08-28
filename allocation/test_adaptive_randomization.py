""" Test Cases for Adaptive Randomization module
"""

import pytest
import allocation.adaptive_randomization as r


def test_double_biased_coin_minimize():
    """ Test Cases for double_biased_coin_minimize """
    result = r.double_biased_coin_minimize(5, 6, 7, 8)
    assert result in ["Control", "Treatment"]

    # Test that you cannot have more events than subjects.
    with pytest.raises(ValueError):
        r.double_biased_coin_minimize(6, 5, 7, 8)
    with pytest.raises(ValueError):
        r.double_biased_coin_minimize(6, 7, 9, 8)
    with pytest.raises(ValueError):
        r.double_biased_coin_minimize(6, 5, 7, 5)

    # Test that you can have the same number of events as subjects
    result = r.double_biased_coin_minimize(6, 6, 7, 8)
    assert result in ["Control", "Treatment"]

    result = r.double_biased_coin_minimize(6, 8, 7, 7)
    assert result in ["Control", "Treatment"]

    result = r.double_biased_coin_minimize(6, 6, 7, 8)
    assert result in ["Control", "Treatment"]


def test_double_biased_coin_urn():
    """ Test Cases for double_biased_coin_urn """
    result = r.double_biased_coin_urn(5, 6, 7, 8)
    assert result in ["Control", "Treatment"]

    # Test that you cannot have more events than subjects.
    with pytest.raises(ValueError):
        r.double_biased_coin_urn(6, 5, 7, 8)
    with pytest.raises(ValueError):
        r.double_biased_coin_urn(6, 7, 9, 8)
    with pytest.raises(ValueError):
        r.double_biased_coin_urn(6, 5, 7, 5)

    # Test that you can have the same number of events as subjects
    result = r.double_biased_coin_urn(6, 6, 7, 8)
    assert result in ["Control", "Treatment"]

    result = r.double_biased_coin_urn(6, 8, 7, 7)
    assert result in ["Control", "Treatment"]

    result = r.double_biased_coin_urn(6, 6, 7, 8)
    assert result in ["Control", "Treatment"]
