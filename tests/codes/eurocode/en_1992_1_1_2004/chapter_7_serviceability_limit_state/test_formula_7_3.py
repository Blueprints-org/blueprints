"""Testing formula 7.3 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_3 import Form7Dot3CoefficientKc


class TestForm7Dot3CoefficientKc:
    """Validation for formula 7.3 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        f_cr = 457  # KN
        a_ct = 100 * 500  # mm²
        f_ct_eff = 2.9  # MPa
        form_7_3 = Form7Dot3CoefficientKc(f_cr=f_cr, a_ct=a_ct, f_ct_eff=f_ct_eff)

        # expected result, is manually calculated
        manually_calculated_result = 2.83655

        assert form_7_3 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_value_under_0_5(self) -> None:
        """Test that the result will not be smaller than 0.5."""
        # example values
        f_cr = 5  # KN -> This is a very small value, and will result in a very small kc value
        a_ct = 100 * 500  # mm²
        f_ct_eff = 2.9  # MPa
        form_7_3 = Form7Dot3CoefficientKc(f_cr=f_cr, a_ct=a_ct, f_ct_eff=f_ct_eff)

        assert form_7_3 == pytest.approx(expected=0.5, rel=1e-4)

    def test_raise_error_negative_a_ct(self) -> None:
        """Test that an error is raised when a_ct is negative."""
        # example values
        f_cr = 457
        a_ct = -1
        f_ct_eff = 2.9
        with pytest.raises(ValueError):
            Form7Dot3CoefficientKc(f_cr=f_cr, a_ct=a_ct, f_ct_eff=f_ct_eff)

    def test_raise_error_negative_f_ct_eff(self) -> None:
        """Test that an error is raised when f_ct_eff is negative."""
        # example values
        f_cr = 457
        a_ct = 100 * 500
        f_ct_eff = -1
        with pytest.raises(ValueError):
            Form7Dot3CoefficientKc(f_cr=f_cr, a_ct=a_ct, f_ct_eff=f_ct_eff)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_c = \max\left(0.9 \cdot \frac{F_{cr}}{A_{ct} \cdot f_{ct,eff}}, 0.5\right) = "
                r"\max\left(0.9 \cdot \frac{457.000}{50000.000 \cdot 2.900}, 0.5\right) = 2.837 \ -",
            ),
            ("short", r"k_c = 2.837 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cr = 457
        a_ct = 100 * 500
        f_ct_eff = 2.9

        # Object to test
        form_7_3_latex = Form7Dot3CoefficientKc(f_cr=f_cr, a_ct=a_ct, f_ct_eff=f_ct_eff).latex()

        actual = {"complete": form_7_3_latex.complete, "short": form_7_3_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
