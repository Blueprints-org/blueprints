"""Testing formula 8.109 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_109 import (
    Form8Dot109MaximumPunchingShearResistance,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot109MaximumPunchingShearResistance:
    """Validation for formula 8.109 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        eta_sys = 1.15
        tau_rd_c = 0.87

        # Object to test
        formula = Form8Dot109MaximumPunchingShearResistance(eta_sys=eta_sys, tau_rd_c=tau_rd_c)

        # Expected result, manually calculated
        manually_calculated_result = 1.0005  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("eta_sys", "tau_rd_c"),
        [
            (-1.15, 0.87),  # eta_sys is negative
            (1.15, -0.87),  # tau_rd_c is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, eta_sys: float, tau_rd_c: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot109MaximumPunchingShearResistance(eta_sys=eta_sys, tau_rd_c=tau_rd_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rd,max} = \eta_{sys} \cdot \tau_{Rd,c} = 1.150 \cdot 0.870 = 1.000 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rd,max} = \eta_{sys} \cdot \tau_{Rd,c} = 1.150 \cdot 0.870 \ MPa = 1.000 \ MPa",
            ),
            ("short", r"\tau_{Rd,max} = 1.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        eta_sys = 1.15
        tau_rd_c = 0.87

        # Object to test
        latex = Form8Dot109MaximumPunchingShearResistance(eta_sys=eta_sys, tau_rd_c=tau_rd_c).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
