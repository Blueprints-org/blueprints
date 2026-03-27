"""Testing formula 8.45 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_2023.chapter_8_ultimate_limit_states.formula_8_45 import Form8Dot45StrengthReductionFactor
from blueprints.validations import NegativeValueError


class TestForm8Dot45StrengthReductionFactor:
    """Validation for formula 8.45 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        epsilon_x = 0.002  # dimensionless
        theta = 45.0  # degrees

        # Object to test
        formula = Form8Dot45StrengthReductionFactor(epsilon_x=epsilon_x, theta=theta)

        # Expected result
        expected_result = True

        assert formula == expected_result
        assert formula.unity_check <= 1.0

    @pytest.mark.parametrize(
        ("epsilon_x", "theta"),
        [
            (-0.002, 45.0),  # epsilon_x is negative
        ],
    )
    def test_raise_error_when_epsilon_x_is_negative(self, epsilon_x: float, theta: float) -> None:
        """Test invalid values where epsilon_x is negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot45StrengthReductionFactor(epsilon_x=epsilon_x, theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v \to v = \frac{1}{1.0 + 110 \cdot (\varepsilon_x + (\varepsilon_x + 0.001) \cdot \cot^2 \theta)} \leq 1.0 \to v = \frac{1}{1.0 + 110 \cdot (0.002 + (0.002 + 0.001) \cdot 0.045)} \leq 1.0 \to \left( 0.645 \leq 1.0 \right) \to OK",  # noqa: E501
            ),
            ("short", r"v \to OK"),
            (
                "complete_with_units",
                r"v \to v = \frac{1}{1.0 + 110 \cdot (\varepsilon_x + (\varepsilon_x + 0.001) \cdot \cot^2 \theta)} \leq 1.0 \to v = \frac{1}{1.0 + 110 \cdot (0.002 + (0.002 + 0.001) \cdot 0.045)} \leq 1.0 \to \left( 0.645 \leq 1.0 \right) \to OK",  # noqa: E501
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        epsilon_x = 0.002  # dimensionless
        theta = 45.0  # degrees
        # TODO: Fix issue with double 'to' symbol
        # Object to test
        latex = Form8Dot45StrengthReductionFactor(epsilon_x=epsilon_x, theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
