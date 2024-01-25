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
        # Example values
        assert SubForm8Dot2CoefficientBarDiameter(diameter=16).latex().complete == (
            r"\eta_{\text{2}} = \left{\matrix{\text{1.0} & \text{voor }"
            r"\text{Ø} ≤ \text{32} \\ (\text{132} - \text{Ø}) / \text{100} & "
            r"\text{voor }\text{Ø} > \text{32} }\right. = \text{1.0} = "
            r"\text{1.0}"
        )

        assert str(SubForm8Dot2CoefficientBarDiameter(diameter=16).latex()) == (
            r"\eta_{\text{2}} = \left{\matrix{\text{1.0} & \text{voor }\text{Ø} "
            r"≤ \text{32} \\ (\text{132} - \text{Ø}) / \text{100} & \text{voor }"
            r"\text{Ø} > \text{32} }\right. = \text{1.0} = \text{1.0}"
        )

        assert SubForm8Dot2CoefficientBarDiameter(diameter=64).latex().complete == (
            r"\eta_{\text{2}} = \left{\matrix{\text{1.0} & \text{voor }"
            r"\text{Ø} ≤ \text{32} \\ (\text{132} - \text{Ø}) / \text{100} & "
            r"\text{voor }\text{Ø} > \text{32} }\right. = (\text{132} - "
            r"\text{64}) / \text{100} = \text{0.68}"
        )

        assert SubForm8Dot2CoefficientBarDiameter(diameter=16).latex().short == r"\eta_{\text{2}} = \text{1.0}"
