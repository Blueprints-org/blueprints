"""Testing formula 5.1 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.formula_5_1 import (
    AnalysisType,
    From5Dot1CriteriumDisregardSecondOrderEffects,
)
from blueprints.validations import MismatchSignError


class TestFrom5Dot1CriteriumDisregardSecondOrderEffects:
    """Validation for formula 5.1 from EN 1993-1-1:2005."""

    testdata = [
        (1000000, 100000, AnalysisType.ELASTIC, True, 1),
        (1000000, 110000, AnalysisType.ELASTIC, False, 1.10),
        (1000000, 50000, AnalysisType.PLASTIC, True, 0.75),
        (1000000, 100000, AnalysisType.PLASTIC, False, 1.50)
    ]

    @pytest.mark.parametrize("f_cr,f_ed,analysis_type,exp_result,exp_uc", testdata)
    def test_evaluation(
            self, f_cr: float, f_ed: float, analysis_type: AnalysisType, exp_result: bool, exp_uc: float) -> None:
        form = From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)
        assert form == exp_result
        assert form.unity_check == pytest.approx(exp_uc)

    @pytest.mark.parametrize(
        ("f_cr", "f_ed", "analysis_type"),
        [
            (1000000, -100000, AnalysisType.ELASTIC),  # f_ed is negative
            (-1000000, 100000, AnalysisType.ELASTIC),  # f_cr is negative
        ],
    )
    def test_error_mismatch_sign(
            self, f_cr: float, f_ed: float, analysis_type: AnalysisType) -> None:
        with pytest.raises(MismatchSignError):
            From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)

    @pytest.mark.parametrize(
        ("f_cr", "f_ed", "analysis_type"),
        [
            (1000000, 100000, "elastic"),  # analysis_type is not of type AnalysisType
        ],
    )
    def test_type_error_analysis_type(
            self, f_cr: float, f_ed: float, analysis_type: AnalysisType) -> None:
        with pytest.raises(TypeError):
            From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"CHECK \to \alpha_{cr} = \frac{F_{cr}}{F_{Ed}} \ge limit \to 10.00 = \frac{1000000.00}{100000.00} \ge 10 \to OK"),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representations of the formula."""
        # Example values
        f_cr = 1000000
        f_ed = 100000
        analysis_type = AnalysisType.ELASTIC

        # Create test object
        latex = From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert expected == actual[representation], f"{representation} representation failed."
