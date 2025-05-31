"""Testing formula 5.9 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_9 import Form5Dot9DesignSupportMomentReduction
from blueprints.validations import NegativeValueError


class TestForm5Dot9DesignSupportMomentReduction:
    """Validation for formula 5.9 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ed_sup = 100
        t = 0.3

        # Object to test
        formula = Form5Dot9DesignSupportMomentReduction(f_ed_sup=f_ed_sup, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 3.75  # kNm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_ed_sup", "t"),
        [
            (-100, 0.3),
            (100, -0.3),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, f_ed_sup: float, t: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot9DesignSupportMomentReduction(f_ed_sup=f_ed_sup, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"ΔM_{Ed} = \frac{F_{Ed,sup} \cdot t}{8} = \frac{100 \cdot 0.3}{8} = 3.750",
            ),
            ("short", r"ΔM_{Ed} = 3.750"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ed_sup = 100
        t = 0.3

        # Object to test
        latex = Form5Dot9DesignSupportMomentReduction(f_ed_sup=f_ed_sup, t=t).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
