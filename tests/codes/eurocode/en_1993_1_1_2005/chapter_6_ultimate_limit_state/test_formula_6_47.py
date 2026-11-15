"""Testing formula 6.47 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_47 import (
    Form6Dot47DesignBucklingResistanceClass1And2And3,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot47DesignBucklingResistanceClass1And2And3:
    """Validation for formula 6.47 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        chi = 0.8
        a = 5000.0
        f_y = 355.0
        gamma_m1 = 1.1

        # Object to test
        formula = Form6Dot47DesignBucklingResistanceClass1And2And3(chi=chi, a=a, f_y=f_y, gamma_m1=gamma_m1)

        # Expected result, manually calculated
        # 0.8 * 5000 * 355 / 1.1 = 1420000 / 1.1 = 1290909.0909
        manually_calculated_result = 1290909.0909  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("chi", "a", "f_y", "gamma_m1"),
        [
            (-0.8, 5000.0, 355.0, 1.1),  # chi is negative
            (0.8, -5000.0, 355.0, 1.1),  # a is negative
            (0.8, 5000.0, -355.0, 1.1),  # f_y is negative
            (0.8, 5000.0, 355.0, 0.0),  # gamma_m1 is zero
            (0.8, 5000.0, 355.0, -1.1),  # gamma_m1 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, chi: float, a: float, f_y: float, gamma_m1: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot47DesignBucklingResistanceClass1And2And3(chi=chi, a=a, f_y=f_y, gamma_m1=gamma_m1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"N_{b,Rd} = \frac{\chi \cdot A \cdot f_y}{\gamma_{M1}} = "
                    r"\frac{0.800 \cdot 5000.000 \cdot 355.000}{1.100} = 1290909.091 \ N"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"N_{b,Rd} = \frac{\chi \cdot A \cdot f_y}{\gamma_{M1}} = "
                    r"\frac{0.800 \cdot 5000.000 \ mm^2 \cdot 355.000 \ MPa}{1.100} = 1290909.091 \ N"
                ),
            ),
            ("short", r"N_{b,Rd} = 1290909.091 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        chi = 0.8
        a = 5000.0
        f_y = 355.0
        gamma_m1 = 1.1

        # Object to test
        latex = Form6Dot47DesignBucklingResistanceClass1And2And3(chi=chi, a=a, f_y=f_y, gamma_m1=gamma_m1).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
