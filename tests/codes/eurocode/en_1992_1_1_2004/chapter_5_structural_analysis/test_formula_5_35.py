"""Testing formula 5.35 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_35 import Form5Dot35EffectiveDepth
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot35EffectiveDepth:
    """Validation for formula 5.35 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        h = 300.0
        i_s = 50.0

        # Object to test
        formula = Form5Dot35EffectiveDepth(h=h, i_s=i_s)

        # Expected result, manually calculated
        manually_calculated_result = 200.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("h", "i_s"),
        [
            (-300.0, 50.0),  # h is negative
            (300.0, -50.0),  # i_s is negative
            (0.0, 50.0),  # h is zero
            (300.0, 0.0),  # i_s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, h: float, i_s: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot35EffectiveDepth(h=h, i_s=i_s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"d = \frac{h}{2} + i_s = \frac{300.000}{2} + 50.000 = 200.000 \ mm",
            ),
            ("short", r"d = 200.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        h = 300.0
        i_s = 50.0

        # Object to test
        latex = Form5Dot35EffectiveDepth(h=h, i_s=i_s).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
