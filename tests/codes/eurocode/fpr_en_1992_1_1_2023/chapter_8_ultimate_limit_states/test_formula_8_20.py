"""Testing formula 8.20 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_20 import Form8Dot20MinimumShearStressResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot20MinimumShearStressResistance:
    """Validation for formula 8.20 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        gamma_v = 1.4
        f_ck = 30.0
        f_yd = 435.0
        d_dg = 32.0
        d = 500.0

        # Object to test
        formula = Form8Dot20MinimumShearStressResistance(gamma_v=gamma_v, f_ck=f_ck, f_yd=f_yd, d_dg=d_dg, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.522000  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("gamma_v", "f_ck", "f_yd", "d_dg", "d"),
        [
            (1.4, -30.0, 435.0, 32.0, 500.0),  # f_ck is negative
            (1.4, 30.0, 435.0, -32.0, 500.0),  # d_dg is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, gamma_v: float, f_ck: float, f_yd: float, d_dg: float, d: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot20MinimumShearStressResistance(gamma_v=gamma_v, f_ck=f_ck, f_yd=f_yd, d_dg=d_dg, d=d)

    @pytest.mark.parametrize(
        ("gamma_v", "f_ck", "f_yd", "d_dg", "d"),
        [
            (-1.4, 30.0, 435.0, 32.0, 500.0),  # gamma_v is negative
            (0.0, 30.0, 435.0, 32.0, 500.0),  # gamma_v is zero
            (1.4, 30.0, -435.0, 32.0, 500.0),  # f_yd is negative
            (1.4, 30.0, 0.0, 32.0, 500.0),  # f_yd is zero
            (1.4, 30.0, 435.0, 32.0, -500.0),  # d is negative
            (1.4, 30.0, 435.0, 32.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, gamma_v: float, f_ck: float, f_yd: float, d_dg: float, d: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less.

        All three sit in a denominator: gamma_v and d directly, f_yd inside the square root.
        """
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot20MinimumShearStressResistance(gamma_v=gamma_v, f_ck=f_ck, f_yd=f_yd, d_dg=d_dg, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rdc,min} = \frac{11}{\gamma_V} \cdot \sqrt{\frac{f_{ck}}{f_{yd}} \cdot \frac{d_{dg}}{d}} = "
                    r"\frac{11}{1.400} \cdot \sqrt{\frac{30.000}{435.000} \cdot \frac{32.000}{500.000}} = 0.522 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rdc,min} = \frac{11}{\gamma_V} \cdot \sqrt{\frac{f_{ck}}{f_{yd}} \cdot \frac{d_{dg}}{d}} = "
                    r"\frac{11}{1.400} \cdot \sqrt{\frac{30.000 \ MPa}{435.000 \ MPa} \cdot \frac{32.000 \ mm}{500.000 \ mm}} = 0.522 \ MPa"
                ),
            ),
            ("short", r"\tau_{Rdc,min} = 0.522 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_v = 1.4
        f_ck = 30.0
        f_yd = 435.0
        d_dg = 32.0
        d = 500.0

        # Object to test
        latex = Form8Dot20MinimumShearStressResistance(gamma_v=gamma_v, f_ck=f_ck, f_yd=f_yd, d_dg=d_dg, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
