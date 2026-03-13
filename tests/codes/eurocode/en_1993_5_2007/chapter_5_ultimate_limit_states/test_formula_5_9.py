"""Testing formula 5.9 of EN 1993-5:2007."""

import itertools

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_9 import Form5Dot9ReducedBendingMomentResistance
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot9ReducedBendingMomentResistance:
    """Validation for formula 5.9 from EN 1993-5:2007."""

    @pytest.mark.parametrize(
        ("mc_rd", "expected_value"),
        [
            (400, 99.9779),  # Mv,Rd < Mc,Rd
            (50, 50),  # Mv,Rd < Mc,Rd
        ],
    )
    def test_evaluation(self, mc_rd: float, expected_value: float) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_b = 0.8  # dimensionless
        w_pl = 500 * 1e3  # mm³
        rho = 0.25  # dimensionless
        a_v = 100  # mm²
        t_w = 10  # mm
        alpha = 45  # degrees
        f_y = 250  # MPa
        gamma_m_0 = 1.0  # dimensionless

        form = Form5Dot9ReducedBendingMomentResistance(
            beta_b=beta_b,
            w_pl=w_pl,
            rho=rho,
            a_v=a_v,
            t_w=t_w,
            alpha=alpha,
            f_y=f_y,
            gamma_m_0=gamma_m_0,
            mc_rd=mc_rd,
        )

        assert form == pytest.approx(expected_value)

    @pytest.mark.parametrize(
        ("invalid_argument", "invalid_value"),
        itertools.product(("beta_b", "w_pl", "rho", "a_v", "t_w", "alpha", "f_y", "gamma_m_0", "mc_rd"), (-1.0, 0.0)),
    )
    def test_raise_error_when_invalid_values_are_given(self, invalid_argument: str, invalid_value: float) -> None:
        """Test a zero and negative value for parameters."""
        kwargs = {
            key: (invalid_value if key == invalid_argument else 1.0)
            for key in ("beta_b", "w_pl", "rho", "a_v", "t_w", "alpha", "f_y", "gamma_m_0", "mc_rd")
        }
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot9ReducedBendingMomentResistance(**kwargs)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{V,Rd} = \min \left\{\left(\beta_b \cdot W_{pl} - \frac{\rho \cdot A_v^2}{4 \cdot t_w \cdot \sin(\alpha)}\right) \cdot "
                r"\frac{f_y}{\gamma_{M0}}, M_{c,Rd}\right\} "
                r"= \min \left\{\left(0.90 \cdot 3070000.00 - \frac{0.01 \cdot 7805.00^2}{4 \cdot 12.20 \cdot "
                r"\sin(55.00)}\right) \cdot \frac{355.00}{0.81} \cdot 10^{-6}, 1500.00\right\} = 1204.27",
            ),
            ("short", r"M_{V,Rd} = 1204.27"),
            (
                "string",
                r"M_{V,Rd} = \min \left\{\left(\beta_b \cdot W_{pl} - \frac{\rho \cdot A_v^2}{4 \cdot t_w \cdot \sin(\alpha)}\right) \cdot "
                r"\frac{f_y}{\gamma_{M0}}, M_{c,Rd}\right\} "
                r"= \min \left\{\left(0.90 \cdot 3070000.00 - \frac{0.01 \cdot 7805.00^2}{4 \cdot 12.20 \cdot "
                r"\sin(55.00)}\right) \cdot \frac{355.00}{0.81} \cdot 10^{-6}, 1500.00\right\} = 1204.27",
            ),
        ],
    )
    def test_latex_output(self, representation: str, expected: str) -> None:
        """Test the latex implementation."""
        beta_b = 0.9  # dimensionless
        w_pl = 3070 * 1e3  # mm³
        rho = 0.01  # dimensionless
        a_v = 7805  # mm²
        t_w = 12.2  # mm
        alpha = 55  # degrees
        f_y = 355  # MPa
        gamma_m_0 = 0.81  # dimensionless
        mc_rd = 1500  # kNm

        form = Form5Dot9ReducedBendingMomentResistance(
            beta_b=beta_b,
            w_pl=w_pl,
            rho=rho,
            a_v=a_v,
            t_w=t_w,
            alpha=alpha,
            f_y=f_y,
            gamma_m_0=gamma_m_0,
            mc_rd=mc_rd,
        ).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected, f"{representation} representation failed."
