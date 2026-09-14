"""Testing formula 8.28 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_28 import (
    Form8Dot28LongitudinalReinforcementRatio,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot28LongitudinalReinforcementRatio:
    """Validation for formula 8.28 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sl = 1500.0
        b_w = 300.0
        d = 500.0

        # Object to test
        formula = Form8Dot28LongitudinalReinforcementRatio(a_sl=a_sl, b_w=b_w, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.01  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_sl", "b_w", "d"),
        [
            (-1500.0, 300.0, 500.0),  # a_sl is negative
            (1500.0, -300.0, 500.0),  # b_w is negative
            (1500.0, 0.0, 500.0),  # b_w is zero
            (1500.0, 300.0, -500.0),  # d is negative
            (1500.0, 300.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sl: float, b_w: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot28LongitudinalReinforcementRatio(a_sl=a_sl, b_w=b_w, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_l = \frac{A_{sl}}{b_w \cdot d} = \frac{1500.000}{300.000 \cdot 500.000} = 0.010 \ -",
            ),
            (
                "complete_with_units",
                r"\rho_l = \frac{A_{sl}}{b_w \cdot d} = \frac{1500.000 \ mm^2}{300.000 \ mm \cdot 500.000 \ mm} = 0.010 \ -",
            ),
            ("short", r"\rho_l = 0.010 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sl = 1500.0
        b_w = 300.0
        d = 500.0

        # Object to test
        latex = Form8Dot28LongitudinalReinforcementRatio(a_sl=a_sl, b_w=b_w, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
