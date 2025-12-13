"""Tests for CheckResult data class."""

import pytest

from blueprints.checks.check_result import CheckResult


class TestCheckResult:
    """Tests for the CheckResult data class."""

    def test_basic(self) -> None:
        """Test creation of CheckResult with both utilization and factor_of_safety."""
        result = CheckResult(
            is_ok=True,
            utilization=0.5,
            factor_of_safety=2.0,
            required=1200.0,
            provided=1600.0,
        )
        assert result.is_ok is True
        assert result.utilization == 0.5
        assert result.factor_of_safety == 2.0
        assert result.required == 1200.0
        assert result.provided == 1600.0

    def test_utilization_equals_zero(self) -> None:
        """Test creation of CheckResult with utilization equal to zero."""
        result = CheckResult(
            is_ok=True,
            utilization=0.0,
            factor_of_safety=None,
            required=1000.0,
            provided=2000.0,
        )
        assert result.is_ok is True
        assert result.utilization == 0.0
        assert result.factor_of_safety == float("inf")  # Infinite safety factor

    def test_utilization_only(self) -> None:
        """Test creation of CheckResult with only utilization given."""
        result = CheckResult(
            is_ok=False,
            utilization=1.25,
            factor_of_safety=None,
            required=None,
            provided=None,
        )
        assert result.is_ok is False
        assert result.utilization == 1.25
        assert result.factor_of_safety == 0.8  # 1 / 1.25

    def test_factor_of_safety_only(self) -> None:
        """Test creation of CheckResult with only factor_of_safety given."""
        result = CheckResult(
            is_ok=True,
            utilization=None,
            factor_of_safety=4.0,
            required=500.0,
            provided=2000.0,
        )
        assert result.is_ok is True
        assert result.utilization == 0.25  # 1 / 4.0
        assert result.factor_of_safety == 4.0

    def test_failure_inconsistency(self) -> None:
        """Test that inconsistent utilization and factor_of_safety raises ValueError."""
        with pytest.raises(ValueError):
            CheckResult(
                is_ok=False,
                utilization=0.9,
                factor_of_safety=1.5,  # Inconsistent with utilization
                required=None,
                provided=None,
            )
