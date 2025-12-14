"""Tests for CheckResult data class."""

import pytest

from blueprints.checks.check_result import CheckResult
from blueprints.validations import NegativeValueError


class TestCheckResult:
    """Tests for the CheckResult data class."""

    def test_fos_ok(self) -> None:
        """Test creation of CheckResult with FoS is ok case."""
        result = CheckResult(
            factor_of_safety=2,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.5
        assert result.factor_of_safety == 2.0

    def test_fos_not_ok(self) -> None:
        """Test creation of CheckResult with FoS is not ok case."""
        result = CheckResult(
            factor_of_safety=0.5,
        )
        assert result.is_ok is False
        assert result.unity_check == 2.0
        assert result.factor_of_safety == 0.5

    def test_uc_ok(self) -> None:
        """Test creation of CheckResult with uc is ok case."""
        result = CheckResult(
            unity_check=0.5,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.5
        assert result.factor_of_safety == 2.0

    def test_uc_not_ok(self) -> None:
        """Test creation of CheckResult with uc is not ok case."""
        result = CheckResult(
            unity_check=2.0,
        )
        assert result.is_ok is False
        assert result.unity_check == 2.0
        assert result.factor_of_safety == 0.5

    def test_unity_check_equals_zero(self) -> None:
        """Test creation of CheckResult with unity_check equal to zero."""
        result = CheckResult(
            unity_check=0.0,
        )
        assert result.is_ok is True
        assert result.unity_check == 0.0
        assert result.factor_of_safety == float("inf")  # Infinite safety factor

    def test_factor_of_safety_equals_zero(self) -> None:
        """Test creation of CheckResult with factor_of_safety equal to zero."""
        result = CheckResult(
            factor_of_safety=0.0,
        )
        assert result.is_ok is False
        assert result.unity_check == float("inf")  # Infinite unity check
        assert result.factor_of_safety == 0.0

    def test_negative_unity_check(self) -> None:
        """Test that negative unity_check raises ValueError."""
        with pytest.raises(NegativeValueError):
            CheckResult(
                unity_check=-0.5,
            )

    def test_negative_factor_of_safety(self) -> None:
        """Test that negative factor_of_safety raises ValueError."""
        with pytest.raises(NegativeValueError):
            CheckResult(
                factor_of_safety=-2.0,
            )

    def test_failure_inconsistency_uc_with_fos(self) -> None:
        """Test that inconsistent unity_check and factor_of_safety raises ValueError."""
        with pytest.raises(ValueError):
            CheckResult(
                is_ok=False,
                unity_check=0.9,
                factor_of_safety=1.5,  # Inconsistent with unity_check
            )

    def test_failure_inconsistency_uc_with_is_ok(self) -> None:
        """Test that inconsistent unity_check and is_ok raises ValueError."""
        with pytest.raises(ValueError):
            CheckResult(
                is_ok=True,
                unity_check=1.2,  # Inconsistent with is_ok
            )

    def test_failure_inconsistency_uc_with_is_not_ok(self) -> None:
        """Test that inconsistent unity_check and is_not_ok raises ValueError."""
        with pytest.raises(ValueError):
            CheckResult(
                is_ok=False,
                unity_check=0.8,  # Inconsistent with is_ok
            )

    def test_failure_inconsistency_fos_with_is_ok(self) -> None:
        """Test that inconsistent factor_of_safety and is_ok raises ValueError."""
        with pytest.raises(ValueError):
            CheckResult(
                is_ok=True,
                factor_of_safety=0.8,  # Inconsistent with is_ok
            )

    def test_failure_inconsistency_fos_with_is_not_ok(self) -> None:
        """Test that inconsistent factor_of_safety and is_not_ok raises ValueError."""
        with pytest.raises(ValueError):
            CheckResult(
                is_ok=False,
                factor_of_safety=1.2,  # Inconsistent with is_ok
            )
