"""Testing sub-formulas for 8.2 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_2 import (
    SubForm8Dot2CoefficientBarDiameter,
)
from blueprints.validations import NegativeValueError


class TestSubForm8Dot2CoefficientBarDiameter:
    """Validation for sub-formula 8.2 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation_small_diameter(self) -> None:
        """Test the evaluation of the result for diameters smaller than 32 mm."""
        diameter = 16  # str
        sub_form_8_2_3 = SubForm8Dot2CoefficientBarDiameter(diameter=diameter)

        # Expected result, manually calculated
        manually_result = 1
        assert sub_form_8_2_3 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_evaluation_large_diameter(self) -> None:
        """Test the evaluation of the result for diameters larger than 32 mm."""
        diameter = 40  # str
        sub_form_8_2_4 = SubForm8Dot2CoefficientBarDiameter(diameter=diameter)

        # Expected result, manually calculated
        manually_result = 0.92
        assert sub_form_8_2_4 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_negative_diameter_is_given(self) -> None:
        """Test an invalid bond quality."""
        # Example values
        diameter = -1  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot2CoefficientBarDiameter(diameter=diameter)

    def test_latex(self) -> None:
        """Test the latex representation."""
        latex_16 = SubForm8Dot2CoefficientBarDiameter(diameter=16).latex()
        latex_64 = SubForm8Dot2CoefficientBarDiameter(diameter=64).latex()
        assert latex_16.complete == r"\eta_2 = \left{\matrix{1.0 & \text{voor }Ø ≤ 32 \\ (132 - Ø) / 100 & \text{voor }Ø > 32 }\right. = 1.0 = 1.00"

        assert str(latex_16) == r"\eta_2 = \left{\matrix{1.0 & \text{voor }Ø ≤ 32 \\ (132 - Ø) / 100 & \text{voor }Ø > 32 }\right. = 1.0 = 1.00"

        assert latex_64.complete == (
            r"\eta_2 = \left{\matrix{1.0 & \text{voor }Ø ≤ 32 \\ (132 - Ø) / 100 & \text{voor }Ø > 32 }\right. = (132 - 64) / 100 = 0.68"
        )

        assert latex_16.short == r"\eta_2 = 1.00"
