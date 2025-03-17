"""Testing formula 6.16 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_6_ultimate_limit_state.formula_6_16 import Form6Dot16NominalWebWidth
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot16NominalWebWidth:
    """Validation for formula 6.16 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        b_w = 300.0
        diameters = [16.0, 20.0, 25.0]

        # Object to test
        formula = Form6Dot16NominalWebWidth(b_w=b_w, diameters=diameters)

        # Expected result, manually calculated
        manually_calculated_result = 269.5  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_w", "diameters"),
        [
            (-300.0, [16.0, 20.0, 25.0]),  # b_w is negative
            (300.0, [-16.0, 20.0, 25.0]),  # one diameter is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_w: float, diameters: list[float]) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot16NominalWebWidth(b_w=b_w, diameters=diameters)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"b_{w,nom} = b_{w} - 0.5 \cdot \sum(⌀) = 300.000 - 0.5 \cdot \left(16.000 + 20.000 + 25.000 \right) = 269.500 mm",
            ),
            ("short", r"b_{w,nom} = 269.500 mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_w = 300.0
        diameters = [16.0, 20.0, 25.0]

        # Object to test
        latex = Form6Dot16NominalWebWidth(b_w=b_w, diameters=diameters).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
