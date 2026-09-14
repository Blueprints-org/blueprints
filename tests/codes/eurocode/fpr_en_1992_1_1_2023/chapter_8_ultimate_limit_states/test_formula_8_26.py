"""Testing formula 8.26 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_26 import (
    Form8Dot26AngleBetweenPrincipalShearForceAndXAxis,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot26AngleBetweenPrincipalShearForceAndXAxis:
    """Validation for formula 8.26 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed_x = 100.0
        v_ed_y = 40.0

        # Object to test
        formula = Form8Dot26AngleBetweenPrincipalShearForceAndXAxis(v_ed_x=v_ed_x, v_ed_y=v_ed_y)

        # Expected result, manually calculated
        manually_calculated_result = 21.801409  # degrees

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "expected"),
        [
            (100.0, 0.0, 0.0),  # shear in the x direction only
            (100.0, 100.0, 45.0),  # equal shear in both directions
        ],
    )
    def test_evaluation_at_characteristic_ratios(self, v_ed_x: float, v_ed_y: float, expected: float) -> None:
        """Tests the evaluation of the result at ratios with an exact angle."""
        formula = Form8Dot26AngleBetweenPrincipalShearForceAndXAxis(v_ed_x=v_ed_x, v_ed_y=v_ed_y)

        assert formula == pytest.approx(expected=expected, abs=1e-9)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y"),
        [
            (100.0, -40.0),  # v_ed_y is negative
            (-100.0, 40.0),  # v_ed_x is negative
            (0.0, 40.0),  # v_ed_x is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed_x: float, v_ed_y: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot26AngleBetweenPrincipalShearForceAndXAxis(v_ed_x=v_ed_x, v_ed_y=v_ed_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\alpha_v = \arctan\left(\frac{v_{Ed,y}}{v_{Ed,x}}\right) = "
                    r"\arctan\left(\frac{40.000}{100.000}\right) = 21.801 \ degrees"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\alpha_v = \arctan\left(\frac{v_{Ed,y}}{v_{Ed,x}}\right) = "
                    r"\arctan\left(\frac{40.000 \ N/mm}{100.000 \ N/mm}\right) = 21.801 \ degrees"
                ),
            ),
            ("short", r"\alpha_v = 21.801 \ degrees"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_x = 100.0
        v_ed_y = 40.0

        # Object to test
        latex = Form8Dot26AngleBetweenPrincipalShearForceAndXAxis(v_ed_x=v_ed_x, v_ed_y=v_ed_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
