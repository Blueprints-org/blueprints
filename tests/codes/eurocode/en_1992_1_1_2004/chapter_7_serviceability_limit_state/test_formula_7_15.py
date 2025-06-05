"""Testing formula 7.15 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_15 import Form7Dot15MaximumCrackSpacing
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot15MaximumCrackSpacing:
    """Validation for formula 7.15 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        theta = 30.0
        sr_max_y = 200.0
        sr_max_z = 300.0

        # Object to test
        formula = Form7Dot15MaximumCrackSpacing(theta=theta, sr_max_y=sr_max_y, sr_max_z=sr_max_z)

        # Expected result, manually calculated
        manually_calculated_result = 166.755778576

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta", "sr_max_y", "sr_max_z"),
        [
            (30.0, 0.0, 300.0),  # sr_max_y is zero
            (30.0, 200.0, 0.0),  # sr_max_z is zero
            (30.0, -200.0, 300.0),  # sr_max_y is negative
            (30.0, 200.0, -300.0),  # sr_max_z is negative
            (-30.0, 200.0, 300.0),  # theta is negative
            (100.0, 200.0, 300.0),  # theta is greater than 90
            (15.0, 200.0, 300.0),  # theta is less than or equal to 15
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, theta: float, sr_max_y: float, sr_max_z: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError, GreaterThan90Error, ValueError)):
            Form7Dot15MaximumCrackSpacing(theta=theta, sr_max_y=sr_max_y, sr_max_z=sr_max_z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{r,max} = \frac{1}{\left(\frac{\cos(\theta)}{s_{r,max,y}}\right) + \left(\frac{\sin(\theta)}{s_{r,max,z}}\right)} = "
                r"\frac{1}{\left(\frac{\cos(30.000)}{200.000}\right) + \left(\frac{\sin(30.000)}{300.000}\right)} = 166.756 \ mm",
            ),
            ("short", r"s_{r,max} = 166.756 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta = 30.0
        sr_max_y = 200.0
        sr_max_z = 300.0

        # Object to test
        latex = Form7Dot15MaximumCrackSpacing(theta=theta, sr_max_y=sr_max_y, sr_max_z=sr_max_z).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
