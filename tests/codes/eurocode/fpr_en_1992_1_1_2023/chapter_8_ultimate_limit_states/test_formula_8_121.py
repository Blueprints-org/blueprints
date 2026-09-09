"""Testing formula 8.121 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_121 import (
    Form8Dot121StrengthReductionFactorCrackedZone,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot121StrengthReductionFactorCrackedZone:
    """Validation for formula 8.121 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example value
        epsilon_1 = 0.005

        # Object to test
        formula = Form8Dot121StrengthReductionFactorCrackedZone(epsilon_1=epsilon_1)

        # Expected result, manually calculated: 1 / (1.0 + 110 * 0.005) = 1 / 1.55
        manually_calculated_result = 0.6451612903225806

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_bound_governs(self) -> None:
        """Tests the evaluation of the result when the upper bound of 1,0 governs."""
        # Example value
        epsilon_1 = 0.0

        # Object to test
        formula = Form8Dot121StrengthReductionFactorCrackedZone(epsilon_1=epsilon_1)

        # Expected result, manually calculated: 1 / (1.0 + 110 * 0.0) = 1.0
        manually_calculated_result = 1.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_epsilon_1_is_negative(self) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot121StrengthReductionFactorCrackedZone(epsilon_1=-0.001)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\nu = \min\left(\frac{1}{1.0 + 110 \cdot \varepsilon_1}, 1.0\right) = "
                    r"\min\left(\frac{1}{1.0 + 110 \cdot 0.005}, 1.0\right) = 0.645 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\nu = \min\left(\frac{1}{1.0 + 110 \cdot \varepsilon_1}, 1.0\right) = "
                    r"\min\left(\frac{1}{1.0 + 110 \cdot 0.005}, 1.0\right) = 0.645 \ -"
                ),
            ),
            ("short", r"\nu = 0.645 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example value
        epsilon_1 = 0.005

        # Object to test
        latex = Form8Dot121StrengthReductionFactorCrackedZone(epsilon_1=epsilon_1).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
