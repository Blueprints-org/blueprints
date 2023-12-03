"""
This module contains pytest tests for validation functions in Blueprints.

It includes tests for:
- raise_if_less_or_equal_to_zero: Ensuring it raises an exception for non-positive values.
- raise_if_negative: Ensuring it raises an exception for negative values.
"""

import pytest

from blueprints.validations import NegativeValueError, NonPositiveValueError, raise_if_less_or_equal_to_zero, raise_if_negative


def test_raise_if_less_or_equal_to_zero_with_positive_values() -> None:
    """Test that no exception is raised for positive values."""
    raise_if_less_or_equal_to_zero(a=1, b=2, c=3)


def test_raise_if_less_or_equal_to_zero_with_zero() -> None:
    """Test that NonPositiveValueError is raised for zero values."""
    with pytest.raises(NonPositiveValueError):
        raise_if_less_or_equal_to_zero(a=0)


def test_raise_if_less_or_equal_to_zero_with_negative() -> None:
    """Test that NonPositiveValueError is raised for negative values."""
    with pytest.raises(NonPositiveValueError):
        raise_if_less_or_equal_to_zero(a=-1)


def test_raise_if_negative_with_positive_values() -> None:
    """Test that no exception is raised for positive values."""
    raise_if_negative(a=1, b=2, c=3)


def test_raise_if_negative_with_zero() -> None:
    """Test that no exception is raised for zero values."""
    raise_if_negative(a=0)


def test_raise_if_negative_with_negative() -> None:
    """Test that NegativeValueError is raised for negative values."""
    with pytest.raises(NegativeValueError):
        raise_if_negative(a=-1)
