"""
Sample tests
"""
import pytest

from app import calc


def test_add_numbers():
    """Test that two numbers are added together."""
    exp = 11
    res = calc.add(3, 8)

    assert res == exp


def test_subtract_numbers():
    """Test that values are subtracted and returned."""
    exp = 7
    res = calc.subtract(3, 10)

    assert res == exp
