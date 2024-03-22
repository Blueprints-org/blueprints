"""Testing formula 5.9 of NEN-EN 1993-5:2008."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states.formula_5_9 import Form5Dot9ReducedBendingMomentResistance
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot9ReducedBendingMomentResistance:
    """Validation for formula 5.9 from NEN-EN 1993-5:2008."""

    @pytest.mark.parametrize(
        ("beta_b", "w_pl", "rho", "a_v", "t_w", "alpha", "f_y", "gamma_m_0", "mc_rd", "expected_value"),
        [
            (0.8, 500, 0.25, 100, 10, 45, 250, 1.0, 400, 99.9779),  # Mv,Rd < Mc,Rd
            (0.8, 500, 0.25, 100, 10, 45, 250, 1.0, 50, 50),  # Mv,Rd < Mc,Rd
        ],
    )
    def test_evaluation(  # noqa: PLR0913
        self,
        beta_b: float,
        w_pl: float,
        rho: float,
        a_v: float,
        t_w: float,
        alpha: float,
        f_y: float,
        gamma_m_0: float,
        mc_rd: float,
        expected_value: float,
    ) -> None:
        """Test the evaluation of the result."""
        form = Form5Dot9ReducedBendingMomentResistance(
            beta_b=beta_b, w_pl=w_pl, rho=rho, a_v=a_v, t_w=t_w, alpha=alpha, f_y=f_y, gamma_m_0=gamma_m_0, mc_rd=mc_rd
        )

        assert form == pytest.approx(expected_value)

    @pytest.mark.parametrize(
        ("beta_b", "w_pl", "rho", "a_v", "t_w", "alpha", "f_y", "gamma_m_0", "mc_rd"),
        [
            (-0.8, 500, 0.25, 100, 10, 45, 250, 1.0, 400),  # beta_b is negative
            (0.8, -500, 0.25, 100, 10, 45, 250, 1.0, 400),  # w_pl is negative
            (0.8, 500, -0.25, 100, 10, 45, 250, 1.0, 400),  # rho is negative
            (0.8, 500, 0.25, -100, 10, 45, 250, 1.0, 400),  # a_v is negative
            (0.8, 500, 0.25, 100, -10, 45, 250, 1.0, 400),  # t_w is negative
            (0.8, 500, 0.25, 100, 10, -45, 250, 1.0, 400),  # alpha is negative
            (0.8, 500, 0.25, 100, 10, 45, 250, -1.0, 400),  # gamma_m_0 is negative
            (0.8, 500, 0.25, 100, 10, 45, 250, 1.0, -400),  # mc_rd is negative
            (0.0, 500, 0.25, 100, 10, 45, 250, 1.0, 400),  # beta_b is zero
            (0.8, 0.0, 0.25, 100, 10, 45, 250, 1.0, 400),  # w_pl is zero
            (0.8, 500, 0.0, 100, 10, 45, 250, 1.0, 400),  # rho is zero
            (0.8, 500, 0.25, 0.0, 10, 45, 250, 1.0, 400),  # a_v is zero
            (0.8, 500, 0.25, 100, 0.0, 45, 250, 1.0, 400),  # t_w is zero
            (0.8, 500, 0.25, 100, 10, 0.0, 250, 1.0, 400),  # alpha is zero
            (0.8, 500, 0.25, 100, 10, 45, 250, 0.0, 400),  # gamma_m_0 is zero
            (0.8, 500, 0.25, 100, 10, 45, 250, 1.0, 0.0),  # mc_rd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(  # noqa: PLR0913
        self, beta_b: float, w_pl: float, rho: float, a_v: float, t_w: float, alpha: float, f_y: float, gamma_m_0: float, mc_rd: float
    ) -> None:
        """Test a zero and negative value for parameters."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot9ReducedBendingMomentResistance(
                beta_b=beta_b, w_pl=w_pl, rho=rho, a_v=a_v, t_w=t_w, alpha=alpha, f_y=f_y, gamma_m_0=gamma_m_0, mc_rd=mc_rd
            )

    def test_latex_output(self) -> None:
        """Test the latex implementation."""
        beta_b = 0.8
        w_pl = 500  # cm³/m
        rho = 0.25
        a_v = 100  # mm²/m
        t_w = 10  # mm
        alpha = 45  # degrees
        f_y = 250  # MPa
        gamma_m_0 = 1.0
        mc_rd = 400  # kNm/m

        form = Form5Dot9ReducedBendingMomentResistance(
            beta_b=beta_b, w_pl=w_pl, rho=rho, a_v=a_v, t_w=t_w, alpha=alpha, f_y=f_y, gamma_m_0=gamma_m_0, mc_rd=mc_rd
        )
        assert (
            form.latex().complete
            == r"M_{V,Rd} = \min \left\{\left(\beta_b \cdot W_{pl} - \frac{\rho \cdot A_v^2}{4 \cdot t_w \cdot \sin(\alpha)}\right) \cdot \frac{f_y}"
            r"{\gamma_{M0}}, M_{c,Rd}\right\} = \min \left\{\left(0.8 \cdot 500 \cdot 10^3 - \frac{0.25 \cdot 100^2}{4 \cdot 10 \cdot "
            r"\sin(45)}\right) \cdot \frac{250}{1.0} \cdot 10^{-6}, 400\right\} = " + str(form)
        )
        assert form.latex().short == r"M_{V,Rd} = " + str(form)
        assert (
            str(form.latex())
            == r"M_{V,Rd} = \min \left\{\left(\beta_b \cdot W_{pl} - \frac{\rho \cdot A_v^2}{4 \cdot t_w \cdot \sin(\alpha)}\right) \cdot \frac{f_y}"
            r"{\gamma_{M0}}, M_{c,Rd}\right\} = \min \left\{\left(0.8 \cdot 500 \cdot 10^3 - \frac{0.25 \cdot 100^2}{4 \cdot 10 \cdot "
            r"\sin(45)}\right) \cdot \frac{250}{1.0} \cdot 10^{-6}, 400\right\} = " + str(form)
        )
