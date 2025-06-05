"""Testing formula 5.7a and 5.7b of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_7ab import Form5Dot7abFlangeEffectiveFlangeWidth
from blueprints.validations import NegativeValueError


class TestForm5Dot7abFlangeEffectiveFlangeWidth:
    """Validation for formula 5.7a and 5.7b from EN 1992-1-1:2004."""

    @pytest.mark.parametrize(
        ("b_i", "l_0", "b_eff_i"),
        [
            (0.4, 3.0, 0.38),
            (0.25, 3.0, 0.25),
            (0.8, 1.5, 0.30),
        ],
    )
    def test_evaluation(self, b_i: float, l_0: float, b_eff_i: float) -> None:
        """Test the evaluation of the result."""
        # Object to test
        form_5_7_ab = Form5Dot7abFlangeEffectiveFlangeWidth(b_i=b_i, l_0=l_0)

        # Expected result, manually calculated
        manually_calculated_result = b_eff_i  # M

        assert form_5_7_ab == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_i", "l_0"),
        [
            (0.4, -3.0),
            (-0.25, 3.0),
            (-0.8, -1.5),
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self,
        b_i: float,
        l_0: float,
    ) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot7abFlangeEffectiveFlangeWidth(b_i=b_i, l_0=l_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"b_{eff,i} = 0.2b_{i}+0.1l_{0} \le 0.2l_{0}\text{ and }b_{eff,i}\le b_{i} = "
                r"0.2\cdot0.4+0.1\cdot3.0 \le 0.2\cdot3.0\text{ and }b_{eff,i}\le 0.4 = 0.380",
            ),
            ("short", r"b_{eff,i} = 0.380"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_i = 0.4  # M
        l_0 = 3.0  # M

        # Object to test
        form_5_7_ab_latex = Form5Dot7abFlangeEffectiveFlangeWidth(b_i=b_i, l_0=l_0).latex()

        actual = {
            "complete": form_5_7_ab_latex.complete,
            "short": form_5_7_ab_latex.short,
        }

        assert expected == actual[representation], f"{representation} representation."
