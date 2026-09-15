"""Testing formula 8.112 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_112 import (
    Form8Dot112OuterControlPerimeterWithoutShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot112OuterControlPerimeterWithoutShearReinforcement:
    """Validation for formula 8.112 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        b_0_5 = 2400.0
        d_v = 200.0
        d_v_out = 180.0
        eta_c = 0.8

        # Object to test
        formula = Form8Dot112OuterControlPerimeterWithoutShearReinforcement(b_0_5=b_0_5, d_v=d_v, d_v_out=d_v_out, eta_c=eta_c)

        # Expected result, manually calculated
        manually_calculated_result = 4629.629630  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_0_5", "d_v", "d_v_out", "eta_c"),
        [
            (-2400.0, 200.0, 180.0, 0.8),  # b_0_5 is negative
            (0.0, 200.0, 180.0, 0.8),  # b_0_5 is zero
            (2400.0, -200.0, 180.0, 0.8),  # d_v is negative
            (2400.0, 0.0, 180.0, 0.8),  # d_v is zero
            (2400.0, 200.0, -180.0, 0.8),  # d_v_out is negative
            (2400.0, 200.0, 0.0, 0.8),  # d_v_out is zero
            (2400.0, 200.0, 180.0, -0.8),  # eta_c is negative
            (2400.0, 200.0, 180.0, 0.0),  # eta_c is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_0_5: float, d_v: float, d_v_out: float, eta_c: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot112OuterControlPerimeterWithoutShearReinforcement(b_0_5=b_0_5, d_v=d_v, d_v_out=d_v_out, eta_c=eta_c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"b_{0,5,out} = b_{0,5} \cdot \left(\frac{d_v}{d_{v,out}} \cdot \frac{1}{\eta_c}\right)^2 = "
                    r"2400.000 \cdot \left(\frac{200.000}{180.000} \cdot \frac{1}{0.800}\right)^2 = 4629.630 \ mm"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"b_{0,5,out} = b_{0,5} \cdot \left(\frac{d_v}{d_{v,out}} \cdot \frac{1}{\eta_c}\right)^2 = "
                    r"2400.000 \ mm \cdot \left(\frac{200.000 \ mm}{180.000 \ mm} \cdot \frac{1}{0.800}\right)^2 = 4629.630 \ mm"
                ),
            ),
            ("short", r"b_{0,5,out} = 4629.630 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_0_5 = 2400.0
        d_v = 200.0
        d_v_out = 180.0
        eta_c = 0.8

        # Object to test
        latex = Form8Dot112OuterControlPerimeterWithoutShearReinforcement(b_0_5=b_0_5, d_v=d_v, d_v_out=d_v_out, eta_c=eta_c).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
