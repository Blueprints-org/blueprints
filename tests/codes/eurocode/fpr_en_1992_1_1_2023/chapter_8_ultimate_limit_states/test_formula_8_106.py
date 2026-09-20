"""Testing formula 8.106 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_106 import (
    Form8Dot106StrengthReductionCoefficientForShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot106StrengthReductionCoefficientForShearReinforcement:
    """Validation for formula 8.106 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        d_v = 250.0
        phi_w = 12.0
        d_dg = 16.0
        eta_c = 0.9
        k_pb = 1.5

        # Object to test
        formula = Form8Dot106StrengthReductionCoefficientForShearReinforcement(d_v=d_v, phi_w=phi_w, d_dg=d_dg, eta_c=eta_c, k_pb=k_pb)

        # Expected result, manually calculated
        manually_calculated_result = 0.763536  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_upper_bound_governs(self) -> None:
        """Tests the evaluation of the result when the upper bound of 0.8 governs."""
        # Example values, with a small d_v and phi_w and a small eta_c * k_pb for the expression to exceed 0.8
        formula = Form8Dot106StrengthReductionCoefficientForShearReinforcement(d_v=50.0, phi_w=6.0, d_dg=32.0, eta_c=0.3, k_pb=1.0)

        # Expected result, manually calculated: the expression yields 18.911736, so the upper bound of 0.8 governs
        manually_calculated_result = 0.8  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d_v", "phi_w", "d_dg", "eta_c", "k_pb"),
        [
            (-250.0, 12.0, 16.0, 0.9, 1.5),  # d_v is negative
            (0.0, 12.0, 16.0, 0.9, 1.5),  # d_v is zero
            (250.0, -12.0, 16.0, 0.9, 1.5),  # phi_w is negative
            (250.0, 0.0, 16.0, 0.9, 1.5),  # phi_w is zero
            (250.0, 12.0, -16.0, 0.9, 1.5),  # d_dg is negative
            (250.0, 12.0, 16.0, -0.9, 1.5),  # eta_c is negative
            (250.0, 12.0, 16.0, 0.0, 1.5),  # eta_c is zero
            (250.0, 12.0, 16.0, 0.9, -1.5),  # k_pb is negative
            (250.0, 12.0, 16.0, 0.9, 0.0),  # k_pb is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d_v: float, phi_w: float, d_dg: float, eta_c: float, k_pb: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot106StrengthReductionCoefficientForShearReinforcement(d_v=d_v, phi_w=phi_w, d_dg=d_dg, eta_c=eta_c, k_pb=k_pb)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\eta_s = \min\left(\frac{d_v}{150 \cdot \phi_w} + \left(15 \cdot \frac{d_{dg}}{d_v}\right)^{\frac{1}{2}} \cdot "
                    r"\left(\frac{1}{\eta_c \cdot k_{pb}}\right)^{\frac{3}{2}}, 0.8\right) = "
                    r"\min\left(\frac{250.000}{150 \cdot 12.000} + \left(15 \cdot \frac{16.000}{250.000}\right)^{\frac{1}{2}} \cdot "
                    r"\left(\frac{1}{0.900 \cdot 1.500}\right)^{\frac{3}{2}}, 0.8\right) = 0.764 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\eta_s = \min\left(\frac{d_v}{150 \cdot \phi_w} + \left(15 \cdot \frac{d_{dg}}{d_v}\right)^{\frac{1}{2}} \cdot "
                    r"\left(\frac{1}{\eta_c \cdot k_{pb}}\right)^{\frac{3}{2}}, 0.8\right) = "
                    r"\min\left(\frac{250.000 \ mm}{150 \cdot 12.000 \ mm} + "
                    r"\left(15 \cdot \frac{16.000 \ mm}{250.000 \ mm}\right)^{\frac{1}{2}} \cdot "
                    r"\left(\frac{1}{0.900 \cdot 1.500}\right)^{\frac{3}{2}}, 0.8\right) = 0.764 \ -"
                ),
            ),
            ("short", r"\eta_s = 0.764 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_v = 250.0
        phi_w = 12.0
        d_dg = 16.0
        eta_c = 0.9
        k_pb = 1.5

        # Object to test
        latex = Form8Dot106StrengthReductionCoefficientForShearReinforcement(d_v=d_v, phi_w=phi_w, d_dg=d_dg, eta_c=eta_c, k_pb=k_pb).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
