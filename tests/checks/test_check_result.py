"""Tests for CheckResult data class."""

import pytest

from blueprints.checks.check_result import CheckResult
from blueprints.validations import NegativeValueError


class TestCheckResult:
    """Tests for the CheckResult data class."""

    def test_from_bool(self) -> None:
        """Test creation of CheckResult from bool parameter."""
        result = CheckResult.from_bool(is_ok=True)
        assert result.is_ok is True
        assert result.unity_check is None
        assert result.factor_of_safety is None
        assert result.provided is None
        assert result.required is None
        assert result.operator == "<="

    def test_from_unity_check(self) -> None:
        """Test creation of CheckResult from unity_check parameter."""
        result = CheckResult.from_unity_check(unity_check=0.75)
        assert result.is_ok is True
        assert result.unity_check == 0.75
        assert result.factor_of_safety == pytest.approx(1.3333, 0.0001)
        assert result.provided is None
        assert result.required is None
        assert result.operator == "<="

    def test_from_factor_of_safety(self) -> None:
        """Test creation of CheckResult from factor_of_safety parameter."""
        result = CheckResult.from_factor_of_safety(factor_of_safety=4.0)
        assert result.is_ok is True
        assert result.unity_check == 0.25
        assert result.factor_of_safety == 4.0
        assert result.provided is None
        assert result.required is None
        assert result.operator == "<="

    @pytest.mark.parametrize(
        ("provided", "operator", "required", "expected_is_ok", "unity_check", "factor_of_safety"),
        [
            (75, "<", 150, True, 0.5, 2.0),  # provided < required
            (75, "<=", 150, True, 0.5, 2.0),
            (75, "==", 150, False, float("inf"), 0.0),
            (75, ">=", 150, False, 2.0, 0.5),
            (75, ">", 150, False, 2.0, 0.5),
            (75, "!=", 150, True, 0.0, float("inf")),
            (100, "<", 100, False, 1.0, 1.0),  # provided == required
            (100, "<=", 100, True, 1.0, 1.0),
            (100, "==", 100, True, 0, float("inf")),
            (100, ">=", 100, True, 1.0, 1.0),
            (100, ">", 100, False, 1.0, 1.0),
            (100, "!=", 100, False, float("inf"), 0.0),
            (150, "<", 75, False, 2.0, 0.5),  # provided > required
            (150, "<=", 75, False, 2.0, 0.5),
            (150, "==", 75, False, float("inf"), 0.0),
            (150, ">=", 75, True, 0.5, 2.0),
            (150, ">", 75, True, 0.5, 2.0),
            (150, "!=", 75, True, 0.0, float("inf")),
            (0, "<", 0, False, float("inf"), 0.0),  # Cases with both zero
            (0, "<=", 0, True, 0.0, float("inf")),
            (0, "==", 0, True, 0.0, float("inf")),
            (0, ">=", 0, True, 0.0, float("inf")),
            (0, ">", 0, False, float("inf"), 0.0),
            (0, "!=", 0, False, float("inf"), 0.0),
            (0, "<", 10, True, 0.0, float("inf")),  # Cases with provided is zero
            (0, "<=", 10, True, 0.0, float("inf")),
            (0, "==", 10, False, float("inf"), 0.0),
            (0, ">=", 10, False, float("inf"), 0.0),
            (0, ">", 10, False, float("inf"), 0.0),
            (0, "!=", 10, True, 0.0, float("inf")),
            (10, "<", 0, False, float("inf"), 0.0),  # Cases with required is zero
            (10, "<=", 0, False, float("inf"), 0.0),
            (10, "==", 0, False, float("inf"), 0.0),
            (10, ">=", 0, True, 0.0, float("inf")),
            (10, ">", 0, True, 0.0, float("inf")),
            (10, "!=", 0, True, 0.0, float("inf")),
            (1e-20, "<", float("inf"), True, 0.0, float("inf")),  # Cases with very small and very large values
            (1e-20, "<=", float("inf"), True, 0.0, float("inf")),
            (1e-20, "==", float("inf"), False, float("inf"), 0.0),
            (1e-20, ">=", float("inf"), False, float("inf"), 0.0),
            (1e-20, ">", float("inf"), False, float("inf"), 0.0),
            (1e-20, "!=", float("inf"), True, 0.0, float("inf")),
            (float("inf"), "<", 1e-20, False, float("inf"), 0.0),  # Reverse cases with very large and very small values
            (float("inf"), "<=", 1e-20, False, float("inf"), 0.0),
            (float("inf"), "==", 1e-20, False, float("inf"), 0.0),
            (float("inf"), ">=", 1e-20, True, 0.0, float("inf")),
            (float("inf"), ">", 1e-20, True, 0.0, float("inf")),
            (float("inf"), "!=", 1e-20, True, 0.0, float("inf")),
        ],
    )
    def test_from_comparison_parametrized(
        self, provided: float, operator: str, required: float, expected_is_ok: bool, unity_check: float, factor_of_safety: float
    ) -> None:
        """Test CheckResult.from_comparison for all operator cases and value relations, including zeros."""
        result = CheckResult.from_comparison(provided=provided, required=required, operator=operator)
        assert result.is_ok == expected_is_ok
        assert result.provided == provided
        assert result.required == required
        assert result.operator == operator
        assert result.unity_check == pytest.approx(unity_check, 0.0001)
        assert result.factor_of_safety == pytest.approx(factor_of_safety, 0.0001)

    @pytest.mark.parametrize(
        "kwargs",
        [
            ({"unity_check": -0.5}),
            ({"factor_of_safety": -2.0}),
            ({"provided": -10, "required": 100}),
            ({"provided": 10, "required": -100}),
            ({"provided": -10, "required": -100}),
        ],
    )
    def test_negative_values_raise(self, kwargs: dict) -> None:
        """Test that negative values for unity_check, factor_of_safety, provided, or required raise NegativeValueError.

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
            ({"is_ok": False, "factor_of_safety": 1.2, "operator": ">"}),
            ({"is_ok": True, "provided": 150, "required": 100}),
            ({"is_ok": False, "provided": 80, "required": 100}),
            ({"is_ok": True, "provided": 100, "required": 100, "operator": ">"}),
            ({"is_ok": True, "provided": 100, "required": 100, "operator": ">", "unity_check": 1.0}),
            ({"is_ok": True, "provided": 80, "required": 100, "operator": ">="}),
            ({"is_ok": False, "provided": 150, "required": 100, "operator": ">="}),
            ({"unity_check": 1.1, "factor_of_safety": 0.5}),
            ({"unity_check": 0.0, "factor_of_safety": 0.0}),
            ({"unity_check": 0.9, "provided": 80, "required": 100}),
            ({"factor_of_safety": 1.1, "provided": 80, "required": 100}),
            ({"provided": 80}),
            ({"required": 100}),
            ({"operator": "NotAnOperator"}),
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
            ({"is_ok": False, "provided": 150, "required": 100}),
            ({"is_ok": True, "provided": 80, "required": 100}),
            ({"is_ok": False, "provided": 80, "required": 100, "operator": ">="}),
            ({"is_ok": True, "provided": 150, "required": 100, "operator": ">="}),
            ({"unity_check": 0.0, "factor_of_safety": float("inf")}),
            ({"unity_check": 2.0, "factor_of_safety": 0.5}),
            ({"unity_check": float("inf"), "factor_of_safety": 0.0}),
            ({"provided": 80, "required": 100, "unity_check": 0.8}),
            ({"provided": 80, "required": 100, "factor_of_safety": 1.25}),
            ({"provided": 80, "required": 100, "operator": "<=", "unity_check": 0.8, "factor_of_safety": 1.25, "is_ok": True}),
        ],
    )
    def test_valid_value_combinations(self, kwargs: dict) -> None:
        """Test that valid combinations produce valid output.

        Parameters
        ----------
            kwargs: Dictionary of arguments to pass to CheckResult.
        """
        assert CheckResult(**kwargs)
