"""Tests for CheckResult data class."""

import pytest

from blueprints.checks.check_result import CheckResult
from blueprints.validations import NegativeValueError


class TestCheckResult:
    """Tests for the CheckResult data class."""

    def test_is_ok_none(self) -> None:
        """Test creation of CheckResult with is_ok as None."""
        result = CheckResult()
        assert result.is_ok is None
        assert result.unity_check is None
        assert result.factor_of_safety is None
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_is_ok_true(self) -> None:
        """Test creation of CheckResult with is_ok as True."""
        result = CheckResult(
            is_ok=True,
        )
        assert result.is_ok is True
        assert result.unity_check is None
        assert result.factor_of_safety is None
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_fos_ok(self) -> None:
        """Test creation of CheckResult with FoS is ok case."""
        result = CheckResult(
            factor_of_safety=2,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.5
        assert result.factor_of_safety == 2.0
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_fos_not_ok(self) -> None:
        """Test creation of CheckResult with FoS is not ok case."""
        result = CheckResult(
            factor_of_safety=0.5,
        )
        assert result.is_ok is False
        assert result.unity_check == 2.0
        assert result.factor_of_safety == 0.5
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_factor_of_safety_equals_zero(self) -> None:
        """Test creation of CheckResult with factor_of_safety equal to zero."""
        result = CheckResult(
            factor_of_safety=0.0,
        )
        assert result.is_ok is False
        assert result.unity_check == float("inf")  # Infinite unity check
        assert result.factor_of_safety == 0.0
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_uc_ok(self) -> None:
        """Test creation of CheckResult with uc is ok case."""
        result = CheckResult(
            unity_check=0.5,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.5
        assert result.factor_of_safety == 2.0
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_uc_not_ok(self) -> None:
        """Test creation of CheckResult with uc is not ok case."""
        result = CheckResult(
            unity_check=2.0,
        )
        assert result.is_ok is False
        assert result.unity_check == 2.0
        assert result.factor_of_safety == 0.5
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_unity_check_equals_zero(self) -> None:
        """Test creation of CheckResult with unity_check equal to zero."""
        result = CheckResult(
            unity_check=0.0,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")  # Infinite safety factor
        assert result.provided is None
        assert result.limit is None
        assert result.operator == "<="

    def test_provided_limit_ok(self) -> None:
        """Test creation of CheckResult with provided and limit indicating ok."""
        result = CheckResult(
            provided=50,
            limit=100,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.5
        assert result.factor_of_safety == 2.0
        assert result.provided == 50
        assert result.limit == 100
        assert result.operator == "<="

    def test_provided_limit_not_ok(self) -> None:
        """Test creation of CheckResult with provided and limit indicating not ok."""
        result = CheckResult(
            provided=200,
            limit=100,
        )
        assert result.is_ok is False
        assert result.unity_check == 2.0
        assert result.factor_of_safety == 0.5
        assert result.provided == 200
        assert result.limit == 100
        assert result.operator == "<="

    def test_provided_limit_ok_swapped_operator(self) -> None:
        """Test creation of CheckResult with provided and limit indicating ok with swapped operator."""
        result = CheckResult(
            provided=200,
            limit=100,
            operator=">=",
        )
        assert result.is_ok is True
        assert result.unity_check == 0.5
        assert result.factor_of_safety == 2.0
        assert result.provided == 200
        assert result.limit == 100
        assert result.operator == ">="

    def test_provided_limit_not_ok_swapped_operator(self) -> None:
        """Test creation of CheckResult with provided and limit indicating not ok with swapped operator."""
        result = CheckResult(
            provided=50,
            limit=100,
            operator=">=",
        )
        assert result.is_ok is False
        assert result.unity_check == 2.0
        assert result.factor_of_safety == 0.5
        assert result.provided == 50
        assert result.limit == 100
        assert result.operator == ">="

    def test_provided_limit_zero(self) -> None:
        """Test creation of CheckResult with provided and limit equal to zero."""
        result = CheckResult(
            provided=0,
            limit=0,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")
        assert result.provided == 0
        assert result.limit == 0
        assert result.operator == "<="

    @pytest.mark.parametrize(
        "kwargs",
        [
            ({"unity_check": -0.5}),
            ({"factor_of_safety": -2.0}),
            ({"provided": -10, "limit": 100}),
            ({"provided": 10, "limit": -100}),
            ({"provided": -10, "limit": -100}),
        ],
    )
    def test_negative_values_raise(self, kwargs: dict) -> None:
        """Test that negative values for unity_check, factor_of_safety, provided, or limit raise NegativeValueError.

        Parameters
        ----------
            kwargs: Dictionary of arguments to pass to CheckResult.
        """
        with pytest.raises(NegativeValueError):
            CheckResult(**kwargs)

    @pytest.mark.parametrize(
        "kwargs",
        [
            ({"is_ok": True, "unity_check": 1.5}),
            ({"is_ok": False, "unity_check": 0.8}),
            ({"is_ok": True, "factor_of_safety": 0.8}),
            ({"is_ok": False, "factor_of_safety": 1.2}),
            ({"is_ok": True, "provided": 150, "limit": 100}),
            ({"is_ok": False, "provided": 80, "limit": 100}),
            ({"is_ok": True, "provided": 80, "limit": 100, "operator": ">="}),
            ({"is_ok": False, "provided": 150, "limit": 100, "operator": ">="}),
            ({"unity_check": 1.1, "factor_of_safety": 0.5}),
            ({"unity_check": 0.9, "provided": 80, "limit": 100}),
            ({"factor_of_safety": 1.1, "provided": 80, "limit": 100}),
            ({"provided": 80}),
            ({"limit": 100}),
            ({"operator": "=="}),
        ],
    )
    def test_invalid_value_combinations(self, kwargs: dict) -> None:
        """Test that invalid combinations raise ValueError.

        Parameters
        ----------
            kwargs: Dictionary of arguments to pass to CheckResult.
        """
        with pytest.raises(ValueError):
            CheckResult(**kwargs)

    @pytest.mark.parametrize(
        "kwargs",
        [
            ({}),
            ({"is_ok": False, "unity_check": 1.5}),
            ({"is_ok": True, "unity_check": 0.8}),
            ({"is_ok": False, "factor_of_safety": 0.8}),
            ({"is_ok": True, "factor_of_safety": 1.2}),
            ({"is_ok": False, "provided": 150, "limit": 100}),
            ({"is_ok": True, "provided": 80, "limit": 100}),
            ({"is_ok": False, "provided": 80, "limit": 100, "operator": ">="}),
            ({"is_ok": True, "provided": 150, "limit": 100, "operator": ">="}),
            ({"provided": 80, "limit": 100, "unity_check": 0.8}),
            ({"provided": 80, "limit": 100, "factor_of_safety": 1.25}),
        ],
    )
    def test_valid_value_combinations(self, kwargs: dict) -> None:
        """Test that valid combinations produce valid output.

        Parameters
        ----------
            kwargs: Dictionary of arguments to pass to CheckResult.
        """
        assert CheckResult(**kwargs)
