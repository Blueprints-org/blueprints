"""Testing formula 8.32 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_32 import (
    Form8Dot32DesignShearStressResistanceWithNormalForce,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot32DesignShearStressResistanceWithNormalForce:
    """Validation for formula 8.32 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression itself governs."""
        # Example values
        tau_rdc_0 = 0.585935
        k_1 = 0.133333
        sigma_cp = -2.0
        tau_rdc_min = 0.522
        tau_rdc_max = 1.483483

        # Object to test
        formula = Form8Dot32DesignShearStressResistanceWithNormalForce(
            tau_rdc_0=tau_rdc_0, k_1=k_1, sigma_cp=sigma_cp, tau_rdc_min=tau_rdc_min, tau_rdc_max=tau_rdc_max
        )

        # Expected result, manually calculated
        manually_calculated_result = 0.852601  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_lower_bound_governs(self) -> None:
        """Tests the evaluation of the result when the lower bound governs."""
        # Example values, with a tensile normal stress that pushes the expression below the lower bound
        formula = Form8Dot32DesignShearStressResistanceWithNormalForce(
            tau_rdc_0=0.585935, k_1=0.133333, sigma_cp=1.0, tau_rdc_min=0.522, tau_rdc_max=1.483483
        )

        # Expected result, manually calculated: the expression yields 0.452602, so the lower bound governs
        manually_calculated_result = 0.522  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_upper_bound_governs(self) -> None:
        """Tests the evaluation of the result when the upper bound governs."""
        # Example values, with a compressive normal stress that pushes the expression above the upper bound
        formula = Form8Dot32DesignShearStressResistanceWithNormalForce(
            tau_rdc_0=0.585935, k_1=0.133333, sigma_cp=-10.0, tau_rdc_min=0.522, tau_rdc_max=1.483483
        )

        # Expected result, manually calculated: the expression yields 1.919265, so the upper bound governs
        manually_calculated_result = 1.483483  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_a_negative_factor(self) -> None:
        """Tests that a negative factor, which Formula (8.34) can produce, is accepted and used as such.

        The inputs are chosen so the result stays between both bounds, otherwise the clamping would hide
        whether the sign of the factor was handled at all.
        """
        formula = Form8Dot32DesignShearStressResistanceWithNormalForce(
            tau_rdc_0=0.585935, k_1=-0.066667, sigma_cp=2.0, tau_rdc_min=0.522, tau_rdc_max=1.483483
        )

        # Expected result, manually calculated: 0.585935 - (-0.066667) * 2.0
        manually_calculated_result = 0.719269  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_rdc_0", "k_1", "sigma_cp", "tau_rdc_min", "tau_rdc_max"),
        [
            (-0.585935, 0.133333, -2.0, 0.522, 1.483483),  # tau_rdc_0 is negative
            (0.585935, 0.133333, -2.0, -0.522, 1.483483),  # tau_rdc_min is negative
            (0.585935, 0.133333, -2.0, 0.522, -1.483483),  # tau_rdc_max is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, tau_rdc_0: float, k_1: float, sigma_cp: float, tau_rdc_min: float, tau_rdc_max: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot32DesignShearStressResistanceWithNormalForce(
                tau_rdc_0=tau_rdc_0, k_1=k_1, sigma_cp=sigma_cp, tau_rdc_min=tau_rdc_min, tau_rdc_max=tau_rdc_max
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rd,c} = \min\left(\max\left(\tau_{Rdc,0} - k_1 \cdot \sigma_{cp}, \tau_{Rdc,min}\right), "
                r"\tau_{Rdc,max}\right) = \min\left(\max\left(0.586 - 0.133 \cdot -2.000, 0.522\right), "
                r"1.483\right) = 0.853 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rd,c} = \min\left(\max\left(\tau_{Rdc,0} - k_1 \cdot \sigma_{cp}, \tau_{Rdc,min}\right), "
                r"\tau_{Rdc,max}\right) = \min\left(\max\left(0.586 \ MPa - 0.133 \cdot -2.000 \ MPa, "
                r"0.522 \ MPa\right), 1.483 \ MPa\right) = 0.853 \ MPa",
            ),
            ("short", r"\tau_{Rd,c} = 0.853 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_rdc_0 = 0.585935
        k_1 = 0.133333
        sigma_cp = -2.0
        tau_rdc_min = 0.522
        tau_rdc_max = 1.483483

        # Object to test
        latex = Form8Dot32DesignShearStressResistanceWithNormalForce(
            tau_rdc_0=tau_rdc_0, k_1=k_1, sigma_cp=sigma_cp, tau_rdc_min=tau_rdc_min, tau_rdc_max=tau_rdc_max
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
