"""Testing formula 8.35 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_35 import (
    Form8Dot35MaximumShearStressResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot35MaximumShearStressResistance:
    """Validation for formula 8.35 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        tau_rdc_0 = 0.585935
        a_cs_0 = 1333.333333
        d = 500.0

        # Object to test
        formula = Form8Dot35MaximumShearStressResistance(tau_rdc_0=tau_rdc_0, a_cs_0=a_cs_0, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 1.483483  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_upper_bound_governs(self) -> None:
        """Tests the evaluation of the result when the printed upper bound governs."""
        # Example values, with a shear span long enough for the expression to exceed 2.7 times tau_rdc_0
        formula = Form8Dot35MaximumShearStressResistance(tau_rdc_0=0.585935, a_cs_0=2500.0, d=500.0)

        # Expected result, manually calculated: 2.7 * 0.585935
        manually_calculated_result = 1.582025  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_rdc_0", "a_cs_0", "d"),
        [
            (0.585935, -1333.333333, 500.0),  # a_cs_0 is negative
            (0.585935, 0.0, 500.0),  # a_cs_0 is zero, which Formula (8.34) also refuses
            (0.585935, 1333.333333, -500.0),  # d is negative
            (0.585935, 1333.333333, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, tau_rdc_0: float, a_cs_0: float, d: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot35MaximumShearStressResistance(tau_rdc_0=tau_rdc_0, a_cs_0=a_cs_0, d=d)

    def test_raise_error_when_negative_values_are_given(self) -> None:
        """The shear stress resistance it scales is the one quantity here that may be zero."""
        with pytest.raises(NegativeValueError):
            Form8Dot35MaximumShearStressResistance(tau_rdc_0=-0.585935, a_cs_0=1333.333333, d=500.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rdc,max} = \min\left(2.15 \cdot \tau_{Rdc,0} \cdot \left(\frac{a_{cs,0}}{d}\right)^{\frac{1}{6}}, "
                r"2.7 \cdot \tau_{Rdc,0}\right) = \min\left(2.15 \cdot 0.586 \cdot "
                r"\left(\frac{1333.333}{500.000}\right)^{\frac{1}{6}}, 2.7 \cdot 0.586\right) = 1.483 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rdc,max} = \min\left(2.15 \cdot \tau_{Rdc,0} \cdot \left(\frac{a_{cs,0}}{d}\right)^{\frac{1}{6}}, "
                r"2.7 \cdot \tau_{Rdc,0}\right) = \min\left(2.15 \cdot 0.586 \ MPa \cdot "
                r"\left(\frac{1333.333 \ mm}{500.000 \ mm}\right)^{\frac{1}{6}}, 2.7 \cdot 0.586 \ MPa\right) = 1.483 \ MPa",
            ),
            ("short", r"\tau_{Rdc,max} = 1.483 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_rdc_0 = 0.585935
        a_cs_0 = 1333.333333
        d = 500.0

        # Object to test
        latex = Form8Dot35MaximumShearStressResistance(tau_rdc_0=tau_rdc_0, a_cs_0=a_cs_0, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
