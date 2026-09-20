"""Testing formula 8.103 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_103 import (
    Form8Dot103FactorKNEccentricTendons,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot103FactorKNEccentricTendons:
    """Validation for formula 8.103 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        b_0 = 600.0
        b_0_5 = 2400.0
        sigma_d = -3.0
        f_ck = 30.0
        e_p = 50.0
        d = 250.0

        # Object to test
        formula = Form8Dot103FactorKNEccentricTendons(b_0=b_0, b_0_5=b_0_5, sigma_d=sigma_d, f_ck=f_ck, e_p=e_p, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 1.324812  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_0", "b_0_5", "sigma_d", "f_ck", "e_p", "d"),
        [
            (-600.0, 2400.0, -3.0, 30.0, 50.0, 250.0),  # b_0 is negative
            (600.0, -2400.0, -3.0, 30.0, 50.0, 250.0),  # b_0_5 is negative
            (600.0, 0.0, -3.0, 30.0, 50.0, 250.0),  # b_0_5 is zero
            (600.0, 2400.0, -3.0, -30.0, 50.0, 250.0),  # f_ck is negative
            (600.0, 2400.0, -3.0, 0.0, 50.0, 250.0),  # f_ck is zero
            (600.0, 2400.0, -3.0, 30.0, 50.0, -250.0),  # d is negative
            (600.0, 2400.0, -3.0, 30.0, 50.0, 0.0),  # d is zero
            (2400.0, 2400.0, -3.0, 30.0, 50.0, 250.0),  # b_0 equals b_0_5, denominator becomes zero
            (3000.0, 2400.0, -3.0, 30.0, 50.0, 250.0),  # b_0 exceeds b_0_5, denominator becomes negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_0: float, b_0_5: float, sigma_d: float, f_ck: float, e_p: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot103FactorKNEccentricTendons(b_0=b_0, b_0_5=b_0_5, sigma_d=sigma_d, f_ck=f_ck, e_p=e_p, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"k_N = \sqrt{1 + \frac{0.47}{1 - b_0/b_{0,5}} \cdot \frac{\left|\sigma_d\right|}{\sqrt{f_{ck}}} "
                    r"\cdot \left(1 + 6 \cdot \frac{e_p}{d}\right)} = "
                    r"\sqrt{1 + \frac{0.47}{1 - 600.000/2400.000} \cdot \frac{\left|-3.000\right|}{\sqrt{30.000}} "
                    r"\cdot \left(1 + 6 \cdot \frac{50.000}{250.000}\right)} = 1.325 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"k_N = \sqrt{1 + \frac{0.47}{1 - b_0/b_{0,5}} \cdot \frac{\left|\sigma_d\right|}{\sqrt{f_{ck}}} "
                    r"\cdot \left(1 + 6 \cdot \frac{e_p}{d}\right)} = "
                    r"\sqrt{1 + \frac{0.47}{1 - 600.000 \ mm/2400.000 \ mm} \cdot "
                    r"\frac{\left|-3.000 \ MPa\right|}{\sqrt{30.000 \ MPa}} "
                    r"\cdot \left(1 + 6 \cdot \frac{50.000 \ mm}{250.000 \ mm}\right)} = 1.325 \ -"
                ),
            ),
            ("short", r"k_N = 1.325 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_0 = 600.0
        b_0_5 = 2400.0
        sigma_d = -3.0
        f_ck = 30.0
        e_p = 50.0
        d = 250.0

        # Object to test
        latex = Form8Dot103FactorKNEccentricTendons(b_0=b_0, b_0_5=b_0_5, sigma_d=sigma_d, f_ck=f_ck, e_p=e_p, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
