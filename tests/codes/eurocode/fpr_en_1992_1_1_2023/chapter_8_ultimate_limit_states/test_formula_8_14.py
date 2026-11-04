"""Testing formula 8.14 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_14 import (
    Form8Dot14ConfinementStressCompressionZone,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot14ConfinementStressCompressionZone:
    """Validation for formula 8.14 from FprEN 1992-1-1:2023."""

    def test_evaluation_x_term_governs(self) -> None:
        """Tests the evaluation of the result where the x term governs the minimum."""
        # Example values
        sum_a_s_confx = 200.0
        b_csy = 500.0
        a_s_confy = 300.0
        x_cs = 300.0
        f_yd = 500.0
        s = 100.0

        # Object to test
        formula = Form8Dot14ConfinementStressCompressionZone(sum_a_s_confx=sum_a_s_confx, b_csy=b_csy, a_s_confy=a_s_confy, x_cs=x_cs, f_yd=f_yd, s=s)

        # Expected result, manually calculated: min(200 / 500, 300 / 300) * 500 / 100
        manually_calculated_result = 2.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_y_term_governs(self) -> None:
        """Tests the evaluation of the result where the y term governs the minimum."""
        # Example values
        sum_a_s_confx = 400.0
        b_csy = 500.0
        a_s_confy = 150.0
        x_cs = 300.0
        f_yd = 500.0
        s = 100.0

        # Object to test
        formula = Form8Dot14ConfinementStressCompressionZone(sum_a_s_confx=sum_a_s_confx, b_csy=b_csy, a_s_confy=a_s_confy, x_cs=x_cs, f_yd=f_yd, s=s)

        # Expected result, manually calculated: min(400 / 500, 150 / 300) * 500 / 100
        manually_calculated_result = 2.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sum_a_s_confx", "a_s_confy", "f_yd"),
        [
            (-200.0, 300.0, 500.0),  # sum_a_s_confx is negative
            (200.0, -300.0, 500.0),  # a_s_confy is negative
            (200.0, 300.0, -500.0),  # f_yd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, sum_a_s_confx: float, a_s_confy: float, f_yd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot14ConfinementStressCompressionZone(sum_a_s_confx=sum_a_s_confx, b_csy=500.0, a_s_confy=a_s_confy, x_cs=300.0, f_yd=f_yd, s=100.0)

    @pytest.mark.parametrize(
        ("b_csy", "x_cs", "s"),
        [
            (-500.0, 300.0, 100.0),  # b_csy is negative
            (500.0, -300.0, 100.0),  # x_cs is negative
            (500.0, 300.0, -100.0),  # s is negative
            (500.0, 300.0, 0.0),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_csy: float, x_cs: float, s: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot14ConfinementStressCompressionZone(sum_a_s_confx=200.0, b_csy=b_csy, a_s_confy=300.0, x_cs=x_cs, f_yd=500.0, s=s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\sigma_{c2d} = \min\left(\frac{\Sigma A_{s,confx}}{b_{csy}}, \frac{A_{s,confy}}{x_{cs}}\right) "
                    r"\cdot \frac{f_{yd}}{s} = \min\left(\frac{200.000}{500.000}, \frac{300.000}{300.000}\right) "
                    r"\cdot \frac{500.000}{100.000} = 2.000 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\sigma_{c2d} = \min\left(\frac{\Sigma A_{s,confx}}{b_{csy}}, \frac{A_{s,confy}}{x_{cs}}\right) "
                    r"\cdot \frac{f_{yd}}{s} = \min\left(\frac{200.000 \ mm^2}{500.000 \ mm}, \frac{300.000 \ mm^2}{300.000 \ mm}\right) "
                    r"\cdot \frac{500.000 \ MPa}{100.000 \ mm} = 2.000 \ MPa"
                ),
            ),
            ("short", r"\sigma_{c2d} = 2.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sum_a_s_confx = 200.0
        b_csy = 500.0
        a_s_confy = 300.0
        x_cs = 300.0
        f_yd = 500.0
        s = 100.0

        # Object to test
        latex = Form8Dot14ConfinementStressCompressionZone(
            sum_a_s_confx=sum_a_s_confx, b_csy=b_csy, a_s_confy=a_s_confy, x_cs=x_cs, f_yd=f_yd, s=s
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
