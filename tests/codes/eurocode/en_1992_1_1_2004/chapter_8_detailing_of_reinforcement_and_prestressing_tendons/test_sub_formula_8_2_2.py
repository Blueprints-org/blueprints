"""Testing sub-formulas for 8.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_2 import (
    SubForm8Dot2CoefficientBarDiameter,
)
from blueprints.validations import NegativeValueError


class TestSubForm8Dot2CoefficientBarDiameter:
    """Validation for sub-formula 8.2 from EN 1992-1-1:2004."""

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

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete_latex_16",
                r"\eta_2 = \begin{matrix} 1.0 & \text{for }Ø ≤ 32 \\ (132 - Ø) / 100 & \text{for }Ø > 32  \end{matrix} = 1.00 = 1.00",
            ),
            ("short_latex_16", r"\eta_2 = 1.00"),
            (
                "complete_latex_64",
                r"\eta_2 = \begin{matrix} 1.0 & \text{for }Ø ≤ 32 \\ (132 - Ø) / 100 & " r"\text{for }Ø > 32  \end{matrix} = (132 - 64) / 100 = 0.68",
            ),
            ("short_latex_64", r"\eta_2 = 0.68"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation."""
        latex_16 = SubForm8Dot2CoefficientBarDiameter(diameter=16).latex()
        latex_64 = SubForm8Dot2CoefficientBarDiameter(diameter=64).latex()

        actual = {
            "complete_latex_16": latex_16.complete,
            "short_latex_16": latex_16.short,
            "complete_latex_64": latex_64.complete,
            "short_latex_64": latex_64.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
