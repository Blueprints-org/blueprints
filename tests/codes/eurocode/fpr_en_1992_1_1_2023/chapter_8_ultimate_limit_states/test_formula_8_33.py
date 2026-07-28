"""Testing formula 8.33 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_33 import (
    Form8Dot33ShearStressResistanceWithoutAxialForce,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot33ShearStressResistanceWithoutAxialForce:
    """Validation for formula 8.33 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        gamma_v = 1.4
        rho_l = 0.01
        f_ck = 30.0
        d_dg = 32.0
        d = 500.0

        # Object to test
        formula = Form8Dot33ShearStressResistanceWithoutAxialForce(gamma_v=gamma_v, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.585935  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_without_reinforcement(self) -> None:
        """Tests the evaluation of the result when there is no longitudinal reinforcement."""
        formula = Form8Dot33ShearStressResistanceWithoutAxialForce(gamma_v=1.4, rho_l=0.0, f_ck=30.0, d_dg=32.0, d=500.0)

        assert formula == pytest.approx(expected=0.0, abs=1e-12)

    @pytest.mark.parametrize(
        ("gamma_v", "rho_l", "f_ck", "d_dg", "d"),
        [
            (1.4, -0.01, 30.0, 32.0, 500.0),  # rho_l is negative
            (1.4, 0.01, -30.0, 32.0, 500.0),  # f_ck is negative
            (1.4, 0.01, 30.0, -32.0, 500.0),  # d_dg is negative
            (-1.4, 0.01, 30.0, 32.0, 500.0),  # gamma_v is negative
            (0.0, 0.01, 30.0, 32.0, 500.0),  # gamma_v is zero
            (1.4, 0.01, 30.0, 32.0, -500.0),  # d is negative
            (1.4, 0.01, 30.0, 32.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, gamma_v: float, rho_l: float, f_ck: float, d_dg: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot33ShearStressResistanceWithoutAxialForce(gamma_v=gamma_v, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rdc,0} = \frac{0.66}{\gamma_V} \cdot \left(100 \cdot \rho_l \cdot f_{ck} \cdot "
                r"\frac{d_{dg}}{d}\right)^{\frac{1}{3}} = \frac{0.66}{1.400} \cdot \left(100 \cdot 0.010 \cdot 30.000 \cdot "
                r"\frac{32.000}{500.000}\right)^{\frac{1}{3}} = 0.586 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rdc,0} = \frac{0.66}{\gamma_V} \cdot \left(100 \cdot \rho_l \cdot f_{ck} \cdot "
                r"\frac{d_{dg}}{d}\right)^{\frac{1}{3}} = \frac{0.66}{1.400} \cdot \left(100 \cdot 0.010 \cdot 30.000 \ MPa \cdot "
                r"\frac{32.000 \ mm}{500.000 \ mm}\right)^{\frac{1}{3}} = 0.586 \ MPa",
            ),
            ("short", r"\tau_{Rdc,0} = 0.586 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_v = 1.4
        rho_l = 0.01
        f_ck = 30.0
        d_dg = 32.0
        d = 500.0

        # Object to test
        latex = Form8Dot33ShearStressResistanceWithoutAxialForce(gamma_v=gamma_v, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
