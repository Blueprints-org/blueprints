"""Testing formula 8.72 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_72 import (
    Form8Dot72LongitudinalStrainInTensileFlange,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot72LongitudinalStrainInTensileFlange:
    """Validation for formula 8.72 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_td = 300000.0
        a_st = 1500.0
        e_s = 200000.0

        # Object to test
        formula = Form8Dot72LongitudinalStrainInTensileFlange(f_td=f_td, a_st=a_st, e_s=e_s)

        # Expected result, manually calculated: 300000 / (1500 * 200000)
        manually_calculated_result = 0.001  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_of_the_lower_bound(self) -> None:
        """Tests the lower bound of zero that the standard prints."""
        # Example values, with a compressive force in the chord
        f_td = -300000.0
        a_st = 1500.0
        e_s = 200000.0

        # Object to test
        formula = Form8Dot72LongitudinalStrainInTensileFlange(f_td=f_td, a_st=a_st, e_s=e_s)

        # Expected result, the lower bound printed in the standard
        manually_calculated_result = 0.0  # -

        assert formula == pytest.approx(expected=manually_calculated_result, abs=1e-12)

    @pytest.mark.parametrize(
        ("f_td", "a_st", "e_s"),
        [
            (300000.0, -1500.0, 200000.0),  # a_st is negative
            (300000.0, 0.0, 200000.0),  # a_st is zero
            (300000.0, 1500.0, -200000.0),  # e_s is negative
            (300000.0, 1500.0, 0.0),  # e_s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_td: float, a_st: float, e_s: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot72LongitudinalStrainInTensileFlange(f_td=f_td, a_st=a_st, e_s=e_s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\epsilon_x = \max\left(\frac{F_{td}}{A_{st} \cdot E_s}, 0\right) = "
                    r"\max\left(\frac{300000.0000}{1500.0000 \cdot 200000.0000}, 0\right) = 0.0010 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\epsilon_x = \max\left(\frac{F_{td}}{A_{st} \cdot E_s}, 0\right) = "
                    r"\max\left(\frac{300000.0000 \ N}{1500.0000 \ mm^2 \cdot 200000.0000 \ MPa}, 0\right) = 0.0010 \ -"
                ),
            ),
            ("short", r"\epsilon_x = 0.0010 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_td = 300000.0
        a_st = 1500.0
        e_s = 200000.0

        # Object to test
        latex = Form8Dot72LongitudinalStrainInTensileFlange(f_td=f_td, a_st=a_st, e_s=e_s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
