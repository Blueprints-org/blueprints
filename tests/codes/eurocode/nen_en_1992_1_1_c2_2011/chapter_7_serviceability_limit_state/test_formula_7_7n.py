"""Testing formula 7.7n of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_7n import Form7Dot7nMaxBarDiameterTension
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot7nMaxBarDiameterTension:
    """Validation for formula 7.7n from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        diam_s_star = 16.0
        f_ct_eff = 2.5
        h_cr = 200.0
        h = 500.0
        d = 450.0

        # Object to test
        formula = Form7Dot7nMaxBarDiameterTension(
            diam_s_star=diam_s_star,
            f_ct_eff=f_ct_eff,
            h_cr=h_cr,
            h=h,
            d=d,
        )

        # Expected result, manually calculated
        manually_calculated_result = 6.89655172413793  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("diam_s_star", "f_ct_eff", "h_cr", "h", "d"),
        [
            (-16.0, 2.5, 200.0, 500.0, 450.0),  # diam_s_star is negative
            (16.0, -2.5, 200.0, 500.0, 450.0),  # f_ct_eff is negative
            (16.0, 2.5, -200.0, 500.0, 450.0),  # h_cr is negative
            (16.0, 2.5, 200.0, -500.0, 450.0),  # h is negative
            (16.0, 2.5, 200.0, 500.0, -450.0),  # d is negative
            (16.0, 2.5, 200.0, 500.0, 500.0),  # d is equal to h
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, diam_s_star: float, f_ct_eff: float, h_cr: float, h: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form7Dot7nMaxBarDiameterTension(
                diam_s_star=diam_s_star,
                f_ct_eff=f_ct_eff,
                h_cr=h_cr,
                h=h,
                d=d,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"⌀_s = ⌀^*_s \cdot \left(\frac{f_{ct,eff}}{2.9}\right) \cdot \left(\frac{h_{cr}}{8 \cdot ( h - d)}\right) = "
                r"16.000 \cdot \left(\frac{2.500}{2.9}\right) \cdot \left(\frac{200.000}{8 \cdot ( 500.000 - 450.000)}\right) "
                r"= 6.897 \ mm",
            ),
            ("short", r"⌀_s = 6.897 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        diam_s_star = 16.0
        f_ct_eff = 2.5
        h_cr = 200.0
        h = 500.0
        d = 450.0

        # Object to test
        latex = Form7Dot7nMaxBarDiameterTension(
            diam_s_star=diam_s_star,
            f_ct_eff=f_ct_eff,
            h_cr=h_cr,
            h=h,
            d=d,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
