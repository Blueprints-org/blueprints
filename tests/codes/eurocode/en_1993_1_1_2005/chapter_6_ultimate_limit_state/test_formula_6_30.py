"""Testing formula 6.30 of NEN-EN 1993-1-1+A1:2016."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_30 import Form6Dot30ReducedPlasticResistanceMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot30ReducedPlasticResistanceMoment:
    """Validation for formula 6.30 from NEN-EN 1993-1-1+A1:2016."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        w_pl_y = 500000.0  # mm^3
        rho = 0.5  # dimensionless
        h_w = 300.0  # mm
        t_w = 10.0  # mm
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless
        m_y_c_rd = 1e10  # Nmm

        # Object to test
        formula = Form6Dot30ReducedPlasticResistanceMoment(
            w_pl_y=w_pl_y,
            rho=rho,
            h_w=h_w,
            t_w=t_w,
            f_y=f_y,
            gamma_m0=gamma_m0,
            m_y_c_rd=m_y_c_rd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 137562500.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        w_pl_y = 500000.0  # mm^3
        rho = 0.5  # dimensionless
        h_w = 300.0  # mm
        t_w = 10.0  # mm
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless
        m_y_c_rd = 100.0  # Nmm

        # Object to test
        formula = Form6Dot30ReducedPlasticResistanceMoment(
            w_pl_y=w_pl_y,
            rho=rho,
            h_w=h_w,
            t_w=t_w,
            f_y=f_y,
            gamma_m0=gamma_m0,
            m_y_c_rd=m_y_c_rd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 100.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("w_pl_y", "rho", "h_w", "t_w", "f_y", "gamma_m0", "m_y_c_rd"),
        [
            (-500000.0, 0.5, 300.0, 10.0, 355.0, 1.0, 100000000.0),  # w_pl_y is negative
            (500000.0, -0.5, 300.0, 10.0, 355.0, 1.0, 100000000.0),  # rho is negative
            (500000.0, 0.5, -300.0, 10.0, 355.0, 1.0, 100000000.0),  # h_w is negative
            (500000.0, 0.5, 300.0, -10.0, 355.0, 1.0, 100000000.0),  # t_w is negative
            (500000.0, 0.5, 300.0, 10.0, -355.0, 1.0, 100000000.0),  # f_y is negative
            (500000.0, 0.5, 300.0, 10.0, 355.0, -1.0, 100000000.0),  # gamma_m0 is negative
            (500000.0, 0.5, 300.0, 10.0, 355.0, 1.0, -100000000.0),  # m_y_c_rd is negative
            (500000.0, 0.5, 300.0, 0.0, 355.0, 1.0, 100000000.0),  # t_w is zero
            (500000.0, 0.5, 300.0, 10.0, 355.0, 0.0, 100000000.0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self, w_pl_y: float, rho: float, h_w: float, t_w: float, f_y: float, gamma_m0: float, m_y_c_rd: float
    ) -> None:
        """Test invalid negative values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot30ReducedPlasticResistanceMoment(
                w_pl_y=w_pl_y,
                rho=rho,
                h_w=h_w,
                t_w=t_w,
                f_y=f_y,
                gamma_m0=gamma_m0,
                m_y_c_rd=m_y_c_rd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{y,V,Rd} = \min\left(\frac{\left[W_{pl,y} - \frac{\rho \cdot (h_w \cdot t_w)^2}"
                r"{4 \cdot t_w}\right] \cdot f_y}{\gamma_{M0}}, M_{y,c,Rd}\right) = "
                r"\min\left(\frac{\left[500000.000 - \frac{0.500 \cdot (300.000 \cdot 10.000)^2}"
                r"{4 \cdot 10.000}\right] \cdot 355.000}{1.000}, 10000000000.000\right) = 137562500.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{y,V,Rd} = \min\left(\frac{\left[W_{pl,y} - \frac{\rho \cdot (h_w \cdot t_w)^2}{4 \cdot t_w}\right] "
                r"\cdot f_y}{\gamma_{M0}}, M_{y,c,Rd}\right) = "
                r"\min\left(\frac{\left[500000.000 \ mm^3 - \frac{0.500 \cdot (300.000 \ mm \cdot 10.000 \ mm)^2}"
                r"{4 \cdot 10.000 \ mm}\right] \cdot 355.000 \ MPa}{1.000}, 10000000000.000 \ Nmm\right) = 137562500.000 \ Nmm",
            ),
            ("short", r"M_{y,V,Rd} = 137562500.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        w_pl_y = 500000.0  # mm^3
        rho = 0.5  # dimensionless
        h_w = 300.0  # mm
        t_w = 10.0  # mm
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless
        m_y_c_rd = 1e10  # Nmm

        # Object to test
        latex = Form6Dot30ReducedPlasticResistanceMoment(
            w_pl_y=w_pl_y,
            rho=rho,
            h_w=h_w,
            t_w=t_w,
            f_y=f_y,
            gamma_m0=gamma_m0,
            m_y_c_rd=m_y_c_rd,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
