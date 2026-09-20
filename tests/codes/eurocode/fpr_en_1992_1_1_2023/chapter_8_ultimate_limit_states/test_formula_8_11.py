"""Testing formula 8.11 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_11 import (
    Form8Dot11ConfinementStressCircularSquareSingleConfinement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot11ConfinementStressCircularSquareSingleConfinement:
    """Validation for formula 8.11 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_s_conf = 100.0
        f_yd = 500.0
        b_cs = 300.0
        s = 150.0

        # Object to test
        formula = Form8Dot11ConfinementStressCircularSquareSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_cs=b_cs, s=s)

        # Expected result, manually calculated: 2 * 100 * 500 / (300 * 150)
        manually_calculated_result = 2.2222222222222223

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_s_conf", "f_yd"),
        [
            (-100.0, 500.0),  # a_s_conf is negative
            (100.0, -500.0),  # f_yd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, a_s_conf: float, f_yd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot11ConfinementStressCircularSquareSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_cs=300.0, s=150.0)

    @pytest.mark.parametrize(
        ("b_cs", "s"),
        [
            (-300.0, 150.0),  # b_cs is negative
            (0.0, 150.0),  # b_cs is zero
            (300.0, -150.0),  # s is negative
            (300.0, 0.0),  # s is zero
        ],
    )
    def test_raise_error_when_b_cs_or_s_is_less_or_equal_to_zero(self, b_cs: float, s: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot11ConfinementStressCircularSquareSingleConfinement(a_s_conf=100.0, f_yd=500.0, b_cs=b_cs, s=s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\sigma_{c2d} = \frac{2 \cdot A_{s,conf} \cdot f_{yd}}{b_{cs} \cdot s} = "
                    r"\frac{2 \cdot 100.000 \cdot 500.000}{300.000 \cdot 150.000} = 2.222 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\sigma_{c2d} = \frac{2 \cdot A_{s,conf} \cdot f_{yd}}{b_{cs} \cdot s} = "
                    r"\frac{2 \cdot 100.000 \ mm^2 \cdot 500.000 \ MPa}{300.000 \ mm \cdot 150.000 \ mm} = 2.222 \ MPa"
                ),
            ),
            ("short", r"\sigma_{c2d} = 2.222 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_s_conf = 100.0
        f_yd = 500.0
        b_cs = 300.0
        s = 150.0

        # Object to test
        latex = Form8Dot11ConfinementStressCircularSquareSingleConfinement(a_s_conf=a_s_conf, f_yd=f_yd, b_cs=b_cs, s=s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
