"""Testing formula 8.94 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_94 import (
    Form8Dot94PunchingShearStressResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot94PunchingShearStressResistance:
    """Validation for formula 8.94 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        gamma_v = 1.4
        k_pb = 1.2
        rho_l = 0.01
        f_ck = 30.0
        d_dg = 32.0
        d_v = 200.0

        # Object to test
        formula = Form8Dot94PunchingShearStressResistance(gamma_v=gamma_v, k_pb=k_pb, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, d_v=d_v)

        # Expected result, manually calculated
        manually_calculated_result = 0.867531  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_upper_bound_governs(self) -> None:
        """Tests the evaluation of the result when the upper bound governs."""
        # Example values, with k_pb and rho_l large enough for the expression to exceed the upper bound
        formula = Form8Dot94PunchingShearStressResistance(gamma_v=1.4, k_pb=2.5, rho_l=0.02, f_ck=30.0, d_dg=32.0, d_v=200.0)

        # Expected result, manually calculated: the expression yields 2.277126, so the upper bound of 1.956152 governs
        manually_calculated_result = 1.956152  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("gamma_v", "k_pb", "rho_l", "f_ck", "d_dg", "d_v"),
        [
            (1.4, -1.2, 0.01, 30.0, 32.0, 200.0),  # k_pb is negative
            (1.4, 1.2, -0.01, 30.0, 32.0, 200.0),  # rho_l is negative
            (1.4, 1.2, 0.01, -30.0, 32.0, 200.0),  # f_ck is negative
            (1.4, 1.2, 0.01, 30.0, -32.0, 200.0),  # d_dg is negative
            (-1.4, 1.2, 0.01, 30.0, 32.0, 200.0),  # gamma_v is negative
            (0.0, 1.2, 0.01, 30.0, 32.0, 200.0),  # gamma_v is zero
            (1.4, 1.2, 0.01, 30.0, 32.0, -200.0),  # d_v is negative
            (1.4, 1.2, 0.01, 30.0, 32.0, 0.0),  # d_v is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, gamma_v: float, k_pb: float, rho_l: float, f_ck: float, d_dg: float, d_v: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot94PunchingShearStressResistance(gamma_v=gamma_v, k_pb=k_pb, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, d_v=d_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rd,c} = \min\left(\frac{0.6}{\gamma_V} \cdot k_{pb} \cdot \left(100 \cdot \rho_l \cdot f_{ck} \cdot "
                    r"\frac{d_{dg}}{d_v}\right)^{\frac{1}{3}}, \frac{0.5}{\gamma_V} \cdot \sqrt{f_{ck}}\right) = "
                    r"\min\left(\frac{0.6}{1.400} \cdot 1.200 \cdot \left(100 \cdot 0.010 \cdot 30.000 \cdot "
                    r"\frac{32.000}{200.000}\right)^{\frac{1}{3}}, \frac{0.5}{1.400} \cdot \sqrt{30.000}\right) = 0.868 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rd,c} = \min\left(\frac{0.6}{\gamma_V} \cdot k_{pb} \cdot \left(100 \cdot \rho_l \cdot f_{ck} \cdot "
                    r"\frac{d_{dg}}{d_v}\right)^{\frac{1}{3}}, \frac{0.5}{\gamma_V} \cdot \sqrt{f_{ck}}\right) = "
                    r"\min\left(\frac{0.6}{1.400} \cdot 1.200 \cdot \left(100 \cdot 0.010 \cdot 30.000 \ MPa \cdot "
                    r"\frac{32.000 \ mm}{200.000 \ mm}\right)^{\frac{1}{3}}, \frac{0.5}{1.400} \cdot \sqrt{30.000 \ MPa}\right) = 0.868 \ MPa"
                ),
            ),
            ("short", r"\tau_{Rd,c} = 0.868 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        gamma_v = 1.4
        k_pb = 1.2
        rho_l = 0.01
        f_ck = 30.0
        d_dg = 32.0
        d_v = 200.0

        # Object to test
        latex = Form8Dot94PunchingShearStressResistance(gamma_v=gamma_v, k_pb=k_pb, rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, d_v=d_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
