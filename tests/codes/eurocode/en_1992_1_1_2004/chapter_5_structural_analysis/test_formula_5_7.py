"""Testing formula 5.7 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_7 import Form5Dot7EffectiveFlangeWidth
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_7ab import Form5Dot7abFlangeEffectiveFlangeWidth
from blueprints.validations import NegativeValueError


class TestForm5Dot7EffectiveFlangeWidth:
    """Validation for formula 5.7 from EN 1992-1-1:2004."""

    @pytest.mark.parametrize(
        ("b", "b_eff"),
        [
            (0.8, 0.6),
            (0.55, 0.55),
        ],
    )
    def test_evaluation(self, b: float, b_eff: float) -> None:
        """Test the evaluation of the result."""
        # Example values
        b_eff_i = [0.2, 0.25]  # M
        b_w = 0.15  # M

        # Object to test
        form_5_7 = Form5Dot7EffectiveFlangeWidth(*b_eff_i, b_w=b_w, b=b)

        # Expected result, manually calculated
        manually_calculated_result = b_eff  # M

        assert form_5_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_eff_i", "b_w", "b"),
        [
            ([0.2, -0.25], 5, 0.8),
            ([-0.2, -0.25], 5, 0.8),
            ([0.2, 0.25], -5, 0.8),
            ([0.2, 0.25], 5, -0.8),
            ([-0.2, -0.25], -5, -0.8),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, b_eff_i: list[float], b_w: float, b: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot7EffectiveFlangeWidth(*b_eff_i, b_w=b_w, b=b)

    def test_integration_of_formulas_5_7_and_5_7a_and_5_7b(self) -> None:
        """Test the integration of formulas 5.7a and 5.7b with formula 5.7."""
        # Example values
        b_1 = 0.25  # M
        b_2 = 0.5  # M
        l_0 = 1.5  # M
        b = 0.8  # M
        b_w = 0.15  # M

        b_eff_i = (
            Form5Dot7abFlangeEffectiveFlangeWidth(b_1, l_0),
            Form5Dot7abFlangeEffectiveFlangeWidth(b_2, l_0),
        )
        # Object to test
        form_5_7 = Form5Dot7EffectiveFlangeWidth(*b_eff_i, b_w=b_w, b=b)

        # Expected result, manually calculated
        manually_calculated_result = 0.6  # M

        assert form_5_7 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"b_{eff} = \sum b_{eff,i}+b_w\le b = \sum (0.2+0.25)+0.15\le 0.75 = 0.600",
            ),
            ("short", r"b_{eff} = 0.600"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_eff_i = [0.2, 0.25]  # M
        b_w = 0.15  # M
        b = 0.75  # M

        # Object to test
        form_5_7_latex = Form5Dot7EffectiveFlangeWidth(*b_eff_i, b_w=b_w, b=b).latex()

        actual = {
            "complete": form_5_7_latex.complete,
            "short": form_5_7_latex.short,
        }

        assert expected == actual[representation], f"{representation} representation."
