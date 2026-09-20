"""Testing formula 8.104 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_104 import (
    Form8Dot104PunchingShearStressResistanceWithShearReinforcement,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot104PunchingShearStressResistanceWithShearReinforcement:
    """Validation for formula 8.104 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        eta_c = 0.725
        tau_rd_c = 0.87
        eta_s = 0.763536
        rho_w = 0.002617
        f_ywd = 435.0

        # Object to test
        formula = Form8Dot104PunchingShearStressResistanceWithShearReinforcement(
            eta_c=eta_c, tau_rd_c=tau_rd_c, eta_s=eta_s, rho_w=rho_w, f_ywd=f_ywd
        )

        # Expected result, manually calculated
        manually_calculated_result = 1.499956  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_lower_bound_governs(self) -> None:
        """Tests the evaluation of the result when the lower bound of rho_w * f_ywd governs."""
        # Example values, with eta_c and eta_s small enough for the expression to fall below the bound
        formula = Form8Dot104PunchingShearStressResistanceWithShearReinforcement(eta_c=0.01, tau_rd_c=0.87, eta_s=0.01, rho_w=0.002617, f_ywd=435.0)

        # Expected result, manually calculated: the expression yields 0.020084, so the bound rho_w * f_ywd governs
        manually_calculated_result = 1.138395  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("eta_c", "tau_rd_c", "eta_s", "rho_w", "f_ywd"),
        [
            (-0.725, 0.87, 0.763536, 0.002617, 435.0),  # eta_c is negative
            (0.725, -0.87, 0.763536, 0.002617, 435.0),  # tau_rd_c is negative
            (0.725, 0.87, -0.763536, 0.002617, 435.0),  # eta_s is negative
            (0.725, 0.87, 0.763536, -0.002617, 435.0),  # rho_w is negative
            (0.725, 0.87, 0.763536, 0.002617, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, eta_c: float, tau_rd_c: float, eta_s: float, rho_w: float, f_ywd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot104PunchingShearStressResistanceWithShearReinforcement(eta_c=eta_c, tau_rd_c=tau_rd_c, eta_s=eta_s, rho_w=rho_w, f_ywd=f_ywd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rd,cs} = \max\left(\eta_c \cdot \tau_{Rd,c} + \eta_s \cdot \rho_w \cdot f_{ywd}, \rho_w \cdot f_{ywd}\right) = "
                    r"\max\left(0.725 \cdot 0.870 + 0.764 \cdot 0.003 \cdot 435.000, 0.003 \cdot 435.000\right) = 1.500 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rd,cs} = \max\left(\eta_c \cdot \tau_{Rd,c} + \eta_s \cdot \rho_w \cdot f_{ywd}, \rho_w \cdot f_{ywd}\right) = "
                    r"\max\left(0.725 \cdot 0.870 \ MPa + 0.764 \cdot 0.003 \cdot 435.000 \ MPa, 0.003 \cdot 435.000 \ MPa\right) = 1.500 \ MPa"
                ),
            ),
            ("short", r"\tau_{Rd,cs} = 1.500 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        eta_c = 0.725
        tau_rd_c = 0.87
        eta_s = 0.763536
        rho_w = 0.002617
        f_ywd = 435.0

        # Object to test
        latex = Form8Dot104PunchingShearStressResistanceWithShearReinforcement(
            eta_c=eta_c, tau_rd_c=tau_rd_c, eta_s=eta_s, rho_w=rho_w, f_ywd=f_ywd
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
