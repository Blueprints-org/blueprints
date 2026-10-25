"""Testing formula 8.95 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_95 import (
    Form8Dot95LongitudinalReinforcementRatioPunchingShear,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot95LongitudinalReinforcementRatioPunchingShear:
    """Validation for formula 8.95 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        rho_l_x = 0.012
        rho_l_y = 0.008

        # Object to test
        formula = Form8Dot95LongitudinalReinforcementRatioPunchingShear(rho_l_x=rho_l_x, rho_l_y=rho_l_y)

        # Expected result, manually calculated
        manually_calculated_result = 0.009798  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("rho_l_x", "rho_l_y"),
        [
            (-0.012, 0.008),  # rho_l_x is negative
            (0.012, -0.008),  # rho_l_y is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, rho_l_x: float, rho_l_y: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot95LongitudinalReinforcementRatioPunchingShear(rho_l_x=rho_l_x, rho_l_y=rho_l_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_l = \sqrt{\rho_{l,x} \cdot \rho_{l,y}} = \sqrt{0.012 \cdot 0.008} = 0.010 \ -",
            ),
            (
                "complete_with_units",
                r"\rho_l = \sqrt{\rho_{l,x} \cdot \rho_{l,y}} = \sqrt{0.012 \cdot 0.008} = 0.010 \ -",
            ),
            ("short", r"\rho_l = 0.010 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        rho_l_x = 0.012
        rho_l_y = 0.008

        # Object to test
        latex = Form8Dot95LongitudinalReinforcementRatioPunchingShear(rho_l_x=rho_l_x, rho_l_y=rho_l_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
