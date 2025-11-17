"""Testing math helpers for Blueprints."""

import pytest

from blueprints.math_helpers import angle_to_slope, cot, csc, sec, slope_to_angle
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestCot:
    """Validation for cotangent function."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        x = 45.0
        expected_result = 1.0
        assert cot(x) == pytest.approx(expected_result, rel=1e-4)

    @pytest.mark.parametrize("x", [0.0, -45.0])
    def test_raise_error_when_invalid_values_are_given(self, x: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, GreaterThan90Error)):
            cot(x)


class TestSec:
    """Validation for secant function."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        x = 60.0
        expected_result = 2.0
        assert sec(x) == pytest.approx(expected_result, rel=1e-4)

    @pytest.mark.parametrize("x", [-30.0])
    def test_raise_error_when_invalid_values_are_given(self, x: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, GreaterThan90Error)):
            sec(x)


class TestCsc:
    """Validation for cosecant function."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        x = 30.0
        expected_result = 2.0
        assert csc(x) == pytest.approx(expected_result, rel=1e-4)

    @pytest.mark.parametrize("x", [0.0, -30.0])
    def test_raise_error_when_invalid_values_are_given(self, x: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, GreaterThan90Error)):
            csc(x)


class TestSlopeToAngle:
    """Validation for slope to angle conversion."""

    @pytest.mark.parametrize(("slope", "expected_result"), [(0, 0), (100, 45)])
    def test_evaluation(self, slope: float, expected_result: float) -> None:
        """Tests the evaluation of the result."""
        assert slope_to_angle(slope) == pytest.approx(expected_result, rel=1e-4)


class TestAngleToSlope:
    """Validation for angle to slope conversion."""

    @pytest.mark.parametrize(("angle", "expected_result"), [(0, 0), (45, 100)])
    def test_evaluation(self, angle: float, expected_result: float) -> None:
        """Tests the evaluation of the result."""
        assert angle_to_slope(angle) == pytest.approx(expected_result, rel=1e-4)

    @pytest.mark.parametrize("angle", [-10.0, 100.0])
    def test_raise_error_when_invalid_values_are_given(self, angle: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, GreaterThan90Error)):
            angle_to_slope(angle)
