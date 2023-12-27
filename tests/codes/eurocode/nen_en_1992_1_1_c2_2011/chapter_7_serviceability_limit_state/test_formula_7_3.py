"""Testing formula 7.3 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_7_serviceability_limit_state.formula_7_3 import Form7Dot3CoefficientKc


class TestForm7Dot3CoefficientKc:
    """Validation for formula 7.3 from NEN-EN 1992-1-1+C2:2011."""

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
