"""Testing formula 6.47 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_47 import (
    Form6Dot47PunchingShearResistance,
)
from blueprints.validations import NegativeValueError


class TestForm6Dot47PunchingShearResistance:
    """Validation for formula 6.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_rd_c = 0.18
        k = 1.5
        rho_l = 0.02
        f_ck = 30.0
        k_1 = 0.1
        sigma_cp = 1.0
        v_min = 0.035

        # Object to test
        formula = Form6Dot47PunchingShearResistance(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, v_min=v_min)

        # Expected result, manually calculated
        manually_calculated_result = 1.15701426312  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_rd_c", "k", "rho_l", "f_ck", "k_1", "sigma_cp", "v_min"),
        [
            (-0.18, 1.5, 0.02, 30.0, 0.1, 1.0, 0.035),  # c_rd_c is negative
            (0.18, -1.5, 0.02, 30.0, 0.1, 1.0, 0.035),  # k is negative
            (0.18, 1.5, -0.02, 30.0, 0.1, 1.0, 0.035),  # rho_l is negative
            (0.18, 1.5, 0.02, -30.0, 0.1, 1.0, 0.035),  # f_ck is negative
            (0.18, 1.5, 0.02, 30.0, -0.1, 1.0, 0.035),  # k_1 is negative
            (0.18, 1.5, 0.02, 30.0, 0.1, -1.0, 0.035),  # sigma_cp is negative
            (0.18, 1.5, 0.02, 30.0, 0.1, 1.0, -0.035),  # v_min is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, c_rd_c: float, k: float, rho_l: float, f_ck: float, k_1: float, sigma_cp: float, v_min: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot47PunchingShearResistance(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, v_min=v_min)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Rd,c} = \max \left( C_{Rd,c} \cdot k \cdot (100 \cdot \rho_l \cdot f_{ck})^{1/3} + "
                r"k_1 \cdot \sigma_{cp}, v_{min} + k_1 \cdot \sigma_{cp} \right) = "
                r"\max \left( 0.180 \cdot 1.500 \cdot (100 \cdot 0.020 \cdot 30.000)^{1/3} + "
                r"0.100 \cdot 1.000, 0.035 + 0.100 \cdot 1.000 \right) = 1.157 \ MPa",
            ),
            ("short", r"v_{Rd,c} = 1.157 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_rd_c = 0.18
        k = 1.5
        rho_l = 0.02
        f_ck = 30.0
        k_1 = 0.1
        sigma_cp = 1.0
        v_min = 0.035

        # Object to test
        latex = Form6Dot47PunchingShearResistance(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, v_min=v_min).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
