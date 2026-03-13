"""Testing formula 7.6n of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_6n import Form7Dot6nMaxBarDiameterBending
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot6nMaxBarDiameterBending:
    """Validation for formula 7.6n from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        diam_s_star = 16.0
        f_ct_eff = 2.5
        k_c = 0.8
        h_cr = 200.0
        h = 500.0
        d = 450.0

        # Object to test
        formula = Form7Dot6nMaxBarDiameterBending(
            diam_s_star=diam_s_star,
            f_ct_eff=f_ct_eff,
            k_c=k_c,
            h_cr=h_cr,
            h=h,
            d=d,
        )

        # Expected result, manually calculated
        manually_calculated_result = 22.0689655172414  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("diam_s_star", "f_ct_eff", "k_c", "h_cr", "h", "d"),
        [
            (-16.0, 2.5, 0.8, 200.0, 500.0, 450.0),  # diam_s_star is negative
            (16.0, -2.5, 0.8, 200.0, 500.0, 450.0),  # f_ct_eff is negative
            (16.0, 2.5, -0.8, 200.0, 500.0, 450.0),  # k_c is negative
            (16.0, 2.5, 0.8, -200.0, 500.0, 450.0),  # h_cr is negative
            (16.0, 2.5, 0.8, 200.0, -500.0, 450.0),  # h is negative
            (16.0, 2.5, 0.8, 200.0, 500.0, -450.0),  # d is negative
            (16.0, 2.5, 0.8, 200.0, 500.0, 500.0),  # d equals h
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, diam_s_star: float, f_ct_eff: float, k_c: float, h_cr: float, h: float, d: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot6nMaxBarDiameterBending(
                diam_s_star=diam_s_star,
                f_ct_eff=f_ct_eff,
                k_c=k_c,
                h_cr=h_cr,
                h=h,
                d=d,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"⌀_s = ⌀^*_s \cdot \left(\frac{f_{ct,eff}}{2.9}\right) \cdot \left(\frac{k_c \cdot h_{cr}}{2 \cdot ( h - d)}\right) = "
                r"16.000 \cdot \left(\frac{2.500}{2.9}\right) \cdot \left(\frac{0.800 \cdot 200.000}{2 \cdot ( 500.000 - 450.000)}\right) "
                r"= 22.069 \ mm",
            ),
            ("short", r"⌀_s = 22.069 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        diam_s_star = 16.0
        f_ct_eff = 2.5
        k_c = 0.8
        h_cr = 200.0
        h = 500.0
        d = 450.0

        # Object to test
        latex = Form7Dot6nMaxBarDiameterBending(
            diam_s_star=diam_s_star,
            f_ct_eff=f_ct_eff,
            k_c=k_c,
            h_cr=h_cr,
            h=h,
            d=d,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
