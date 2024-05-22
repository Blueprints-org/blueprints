"""
Pytest tests for validation functions in Blueprints.

It includes tests for:
- raise_if_less_or_equal_to_zero: Ensuring it raises an exception for non-positive values.
- raise_if_negative: Ensuring it raises an exception for negative values.
"""

import pytest

from blueprints.validations import (
    GreaterThan90Error,
    LessOrEqualToZeroError,
    ListsNotSameLengthError,
    NegativeValueError,
    raise_if_greater_than_90,
    raise_if_less_or_equal_to_zero,
    raise_if_lists_differ_in_length,
    raise_if_negative,
)


def test_raise_if_less_or_equal_to_zero_with_positive_values() -> None:
    """Test that no exception is raised for positive values."""
    raise_if_less_or_equal_to_zero(a=1, b=2, c=3)


def test_raise_if_less_or_equal_to_zero_with_zero() -> None:
    """Test that NonPositiveValueError is raised for zero values."""
    with pytest.raises(LessOrEqualToZeroError):
        raise_if_less_or_equal_to_zero(a=0)


def test_raise_if_less_or_equal_to_zero_with_negative() -> None:
    """Test that NonPositiveValueError is raised for negative values."""
    with pytest.raises(LessOrEqualToZeroError):
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


def test_raise_if_greater_90_with_less_than_90() -> None:
    """Test that no exception is raised for values lesser than 90."""
    raise_if_greater_than_90(a=-10, b=0, c=85)


def test_raise_if_greater_90_with_90() -> None:
    """Test that no exception is raised for 90."""
    raise_if_greater_than_90(a=90)


def test_raise_if_greater_90_with_greater_than_90() -> None:
    """Test that GreaterThan90Error is raised for values greater than 90."""
    with pytest.raises(GreaterThan90Error):
        raise_if_greater_than_90(a=95)


def test_raise_if_lists_differ_in_length_with_equal_lengths() -> None:
    """Test that no exception is raised for equal length lists."""
    raise_if_lists_differ_in_length(a=[1, 2], b=[3, 4], c=[5, 6])


def test_raise_if_lists_differ_in_length_with_different_lengths() -> None:
    """Test that ListsNotSameLengthError is raised for lists with different length."""
    with pytest.raises(ListsNotSameLengthError):
        raise_if_lists_differ_in_length(a=[1, 2], b=[3, 4], c=[5, 6, 7])
