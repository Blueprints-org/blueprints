"""Testing formula 8.120 of FprEN 1992-1-1:2023."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_120 import (
    Form8Dot120StrengthReductionFactorUncrackedStrut,
)


class TestForm8Dot120StrengthReductionFactorUncrackedStrut:
    """Validation for formula 8.120 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Object to test
        formula = Form8Dot120StrengthReductionFactorUncrackedStrut()

        # Expected result, as printed in the standard
        manually_calculated_result = 1.0

        assert formula == manually_calculated_result

    def test_latex(self) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot120StrengthReductionFactorUncrackedStrut().latex()

        assert latex.complete == r"\nu = 1.0 = 1.0 = 1.000 \ -"
        assert latex.complete_with_units == r"\nu = 1.0 = 1.0 = 1.000 \ -"
        assert latex.short == r"\nu = 1.000 \ -"
