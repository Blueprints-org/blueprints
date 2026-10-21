"""Testing formula 8.105 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_105 import (
    Form8Dot105StrengthReductionCoefficientForShearResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot105StrengthReductionCoefficientForShearResistance:
    """Validation for formula 8.105 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        tau_rd_c = 0.87
        tau_ed = 1.2

        # Object to test
        formula = Form8Dot105StrengthReductionCoefficientForShearResistance(tau_rd_c=tau_rd_c, tau_ed=tau_ed)

        # Expected result, manually calculated
        manually_calculated_result = 0.725  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_rd_c", "tau_ed"),
        [
            (-0.87, 1.2),  # tau_rd_c is negative
            (0.87, -1.2),  # tau_ed is negative
            (0.87, 0.0),  # tau_ed is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_rd_c: float, tau_ed: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot105StrengthReductionCoefficientForShearResistance(tau_rd_c=tau_rd_c, tau_ed=tau_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\eta_c = \frac{\tau_{Rd,c}}{\tau_{Ed}} = \frac{0.870}{1.200} = 0.725 \ -",
            ),
            (
                "complete_with_units",
                r"\eta_c = \frac{\tau_{Rd,c}}{\tau_{Ed}} = \frac{0.870 \ MPa}{1.200 \ MPa} = 0.725 \ -",
            ),
            ("short", r"\eta_c = 0.725 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_rd_c = 0.87
        tau_ed = 1.2

        # Object to test
        latex = Form8Dot105StrengthReductionCoefficientForShearResistance(tau_rd_c=tau_rd_c, tau_ed=tau_ed).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
