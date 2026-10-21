"""Testing formula 8.71 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_71 import Form8Dot71StrengthReductionFactor


class TestForm8Dot71StrengthReductionFactor:
    """Validation for formula 8.71 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Object to test
        formula = Form8Dot71StrengthReductionFactor()

        # Expected result, the value printed in the standard
        manually_calculated_result = 0.5  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"\nu = 0.5 = 0.500 \ -"),
            ("complete_with_units", r"\nu = 0.5 = 0.500 \ -"),
            ("short", r"\nu = 0.500 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot71StrengthReductionFactor().latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
