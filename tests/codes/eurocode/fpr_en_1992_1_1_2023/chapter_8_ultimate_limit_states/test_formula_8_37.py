"""Testing formula 8.37 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_37 import (
    Form8Dot37ReinforcementRatioPrestressedMembers,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot37ReinforcementRatioPrestressedMembers:
    """Validation for formula 8.37 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d_s = 500.0
        a_s = 1500.0
        d_p = 450.0
        a_p = 800.0
        b_w = 300.0
        d = 483.783784  # from formula 8.36 for the same reinforcement

        # Object to test
        formula = Form8Dot37ReinforcementRatioPrestressedMembers(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p, b_w=b_w, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.015809  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_reduces_to_formula_8_28_without_prestressing(self) -> None:
        """Tests that omitting the prestressed reinforcement reproduces Formula (8.28).

        With a_p = 0 the formula becomes d_s * A_s / (b_w * d_s^2), which is A_s / (b_w * d_s), the
        reinforcement ratio of Formula (8.28) for the same section. The assertion is on exact equality rather
        than on a tolerance, because that reduction is exact and a tolerance would only hide it if it ever
        stopped being.
        """
        formula = Form8Dot37ReinforcementRatioPrestressedMembers(d_s=500.0, a_s=1500.0, d_p=450.0, a_p=0.0, b_w=300.0, d=500.0)

        # 1500 / (300 * 500), the value Formula (8.28) gives for the same section
        assert float(formula) == 0.01

    @pytest.mark.parametrize(
        ("d_s", "a_s", "d_p", "a_p", "b_w", "d"),
        [
            (-500.0, 1500.0, 450.0, 800.0, 300.0, 483.783784),  # d_s is negative
            (500.0, -1500.0, 450.0, 800.0, 300.0, 483.783784),  # a_s is negative
            (500.0, 1500.0, -450.0, 800.0, 300.0, 483.783784),  # d_p is negative
            (500.0, 1500.0, 450.0, -800.0, 300.0, 483.783784),  # a_p is negative
            (500.0, 1500.0, 450.0, 800.0, -300.0, 483.783784),  # b_w is negative
            (500.0, 1500.0, 450.0, 800.0, 0.0, 483.783784),  # b_w is zero
            (500.0, 1500.0, 450.0, 800.0, 300.0, -483.783784),  # d is negative
            (500.0, 1500.0, 450.0, 800.0, 300.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d_s: float, a_s: float, d_p: float, a_p: float, b_w: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot37ReinforcementRatioPrestressedMembers(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p, b_w=b_w, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\rho_l = \frac{d_s \cdot A_s + d_p \cdot A_p}{b_w \cdot \left(d\right)^2} = "
                    r"\frac{500.000 \cdot 1500.000 + 450.000 \cdot 800.000}{300.000 \cdot \left(483.784\right)^2} = 0.016 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\rho_l = \frac{d_s \cdot A_s + d_p \cdot A_p}{b_w \cdot \left(d\right)^2} = "
                    r"\frac{500.000 \ mm \cdot 1500.000 \ mm^2 + 450.000 \ mm \cdot 800.000 \ mm^2}"
                    r"{300.000 \ mm \cdot \left(483.784 \ mm\right)^2} = 0.016 \ -"
                ),
            ),
            ("short", r"\rho_l = 0.016 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_s = 500.0
        a_s = 1500.0
        d_p = 450.0
        a_p = 800.0
        b_w = 300.0
        d = 483.783784

        # Object to test
        latex = Form8Dot37ReinforcementRatioPrestressedMembers(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p, b_w=b_w, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
