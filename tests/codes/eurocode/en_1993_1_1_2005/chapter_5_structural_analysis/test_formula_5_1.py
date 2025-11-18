"""Testing formula 5.1 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.formula_5_1 import From5Dot1CriteriumDisregardSecondOrderEffects, AnalysisType


class TestFrom5Dot1CriteriumDisregardSecondOrderEffects:
    """Validation for formula 5.1 from EN 1993-1-1:2005."""

    testdata = [
        (1000000, 100000, AnalysisType.ELASTIC, True, 1)
    ]

    @pytest.mark.parametrize("f_cr,f_ed,analysis_type,exp_result,exp_uc", testdata)
    def test_evaluation(self, f_cr, f_ed, analysis_type, exp_result, exp_uc):
        form = From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)
        assert form == exp_result
        assert (form.unity_check == exp_uc)

    # def test_evaluation(self) -> None:
    #     """Test the evaluation of the result."""
    #     # Example values
    #     f_cr = 1000000
    #     f_ed = 100000
    #
    #     # Create test object
    #     form = From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=AnalysisType.ELASTIC)
    #
    #     # Expected results
    #     exp_result = True
    #     exp_uc = (f_cr / f_ed) / 10
    #
    #     # Test
    #     assert form == exp_result
    #     assert form.unity_check == exp_uc
    #
    # @pytest.mark.parametrize(
    #     ("h_ed", "v_ed"),
    #     [
    #         (50000, -100000),  # v_ed is negative
    #         (-50000, 100000),  # h_ed is negative
    #     ],
    # )
    # def test_error_when_negative(self, h_ed: float, v_ed: float) -> None:
    #     """Test if correct error is raised when provide negatives or zeroes."""
    #     with pytest.raises(NegativeValueError):
    #         Form5Dot7DisregardFrameSwayImperfections(v_ed=v_ed, h_ed=h_ed)
    #
    # @pytest.mark.parametrize(
    #     ("representation", "expected"),
    #     [
    #         ("complete", r"CHECK \to H_{Ed} \geq 0.15 \cdot V_{Ed} \to 50000.00 \geq 0.15 \cdot 100000.00 \to OK"),
    #         ("short", r"CHECK \to OK"),
    #     ],
    # )
    # def test_latex(self, representation: str, expected: str) -> None:
    #     """Test the latex representations of the formula."""
    #     # Example values
    #     h_ed = 50000
    #     v_ed = 100000
    #
    #     # Create test object
    #     latex = Form5Dot7DisregardFrameSwayImperfections(h_ed=h_ed, v_ed=v_ed).latex()
    #
    #     actual = {"complete": latex.complete, "short": latex.short}
    #
    #     assert expected == actual[representation], f"{representation} representation failed ."