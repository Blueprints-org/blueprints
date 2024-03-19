"""Testing formula 5.7 of NEN-EN 1993-5:2008."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states.formula_5_7 import Form5Dot7ShearBucklingResistance
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot7ShearBucklingResistance:
    """Validation for formula 5.7 from NEN-EN 1993-5:2008."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        h = 500  # MM
        tf = 20  # MM
        tw = 10  # MM
        f_bv = 300  # kN
        gamma_m_0 = 1.1

        form = Form5Dot7ShearBucklingResistance(h=h, tf=tf, tw=tw, f_bv=f_bv, gamma_m_0=gamma_m_0)

        # Expected result, manually calculated
        expected = 1309090.909

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("h", "tf", "tw", "f_bv", "gamma_m_0"),
        [
            (500, -20, 10, 300, 1.1),  # tf is negative
            (500, 0, 10, 300, 1.1),  # tf is zero
            (500, 20, -10, 300, 1.1),  # tw is negative
            (500, 20, 0, 300, 1.1),  # tw is zero
            (500, 20, 10, 300, 0),  # gamma_m_0 is zero
        ],
    )
    def test_raise_error_when_negative_or_zero_values_are_given(self, h: float, tf: float, tw: float, f_bv: float, gamma_m_0: float) -> None:
        """Test a zero and negative value for parameters h, tf, tw, f_bv, and gamma_m_0."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot7ShearBucklingResistance(h=h, tf=tf, tw=tw, f_bv=f_bv, gamma_m_0=gamma_m_0)

    def test_latex_output(self) -> None:
        """Test the latex implementation."""
        h = 500  # MM
        tf = 20  # MM
        tw = 10  # MM
        f_bv = 300  # kN
        gamma_m_0 = 1.1

        form = Form5Dot7ShearBucklingResistance(h=h, tf=tf, tw=tw, f_bv=f_bv, gamma_m_0=gamma_m_0)
        assert form.latex().complete == (
            r"V_{b,Rd} = \frac{\left(h - t_f \right) t_w f_{bv}}{\gamma_{M0}} = \frac{(500 - 20) \cdot 10 \cdot 300}{1.1} = "
        ) + str(form)
        assert form.latex().short == r"V_{b,Rd} = " + str(form)
        assert str(form.latex()) == (
            r"V_{b,Rd} = \frac{\left(h - t_f \right) t_w f_{bv}}{\gamma_{M0}} = \frac{(500 - 20) \cdot 10 \cdot 300}{1.1} = "
        ) + str(form)
