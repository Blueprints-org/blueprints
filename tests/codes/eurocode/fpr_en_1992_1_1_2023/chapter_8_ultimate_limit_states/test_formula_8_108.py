"""Testing formula 8.108 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_108 import (
    Form8Dot108ShearResistingEffectiveDepthOuterShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot108ShearResistingEffectiveDepthOuterShearReinforcement:
    """Validation for formula 8.108 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d_x = 250.0
        d_y = 230.0
        c_v = 20.0

        # Object to test
        formula = Form8Dot108ShearResistingEffectiveDepthOuterShearReinforcement(d_x=d_x, d_y=d_y, c_v=c_v)

        # Expected result, manually calculated
        manually_calculated_result = 220.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d_x", "d_y", "c_v"),
        [
            (-250.0, 230.0, 20.0),  # d_x is negative
            (0.0, 230.0, 20.0),  # d_x is zero
            (250.0, -230.0, 20.0),  # d_y is negative
            (250.0, 0.0, 20.0),  # d_y is zero
            (250.0, 230.0, -20.0),  # c_v is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d_x: float, d_y: float, c_v: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot108ShearResistingEffectiveDepthOuterShearReinforcement(d_x=d_x, d_y=d_y, c_v=c_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"d_{v,out} = \frac{d_x + d_y}{2} - c_v = \frac{250.000 + 230.000}{2} - 20.000 = 220.000 \ mm",
            ),
            (
                "complete_with_units",
                r"d_{v,out} = \frac{d_x + d_y}{2} - c_v = \frac{250.000 \ mm + 230.000 \ mm}{2} - 20.000 \ mm = 220.000 \ mm",
            ),
            ("short", r"d_{v,out} = 220.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_x = 250.0
        d_y = 230.0
        c_v = 20.0

        # Object to test
        latex = Form8Dot108ShearResistingEffectiveDepthOuterShearReinforcement(d_x=d_x, d_y=d_y, c_v=c_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
