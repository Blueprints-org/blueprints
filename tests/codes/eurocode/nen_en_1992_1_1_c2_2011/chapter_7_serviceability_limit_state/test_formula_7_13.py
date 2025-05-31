"""Testing formula 7.13 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_13 import Form7Dot13CoefficientK2
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot13CoefficientK2:
    """Validation for formula 7.13 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        epsilon_1 = 0.002
        epsilon_2 = 0.001

        # Object to test
        formula = Form7Dot13CoefficientK2(epsilon_1=epsilon_1, epsilon_2=epsilon_2)

        # Expected result, manually calculated
        manually_calculated_result = 0.75  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("epsilon_1", "epsilon_2"),
        [
            (0, 0.001),  # epsilon_1 is zero
            (-0.002, 0.001),  # epsilon_1 is negative
            (0.002, -0.001),  # epsilon_2 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, epsilon_1: float, epsilon_2: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form7Dot13CoefficientK2(epsilon_1=epsilon_1, epsilon_2=epsilon_2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_2 = \frac{\epsilon_1 + \epsilon_2}{2 \cdot \epsilon_1} = \frac{0.002 + 0.001}{2 \cdot 0.002} = 0.750 \ -",
            ),
            ("short", r"k_2 = 0.750 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_1 = 0.002
        epsilon_2 = 0.001

        # Object to test
        latex = Form7Dot13CoefficientK2(epsilon_1=epsilon_1, epsilon_2=epsilon_2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
