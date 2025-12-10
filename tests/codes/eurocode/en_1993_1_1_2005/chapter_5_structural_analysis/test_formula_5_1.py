"""Testing formula 5.1 of EN 1993-1-1:2005."""

from typing import ClassVar, Literal

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.formula_5_1 import Form5Dot1CriteriumDisregardSecondOrderEffects
from blueprints.validations import MismatchSignError


class TestForm5Dot1CriteriumDisregardSecondOrderEffects:
    """Validation for formula 5.1 from EN 1993-1-1:2005."""

    testdata: ClassVar[list[tuple[float, float, str, bool, float]]] = [
        (1000000, 100000, "elastic", True, 1),
        (1000000, 110000, "elastic", False, 1.10),
        (1000000, 50000, "plastic", True, 0.75),
        (1000000, 100000, "plastic", False, 1.50),
        (-1000000, -100000, "plastic", False, 1.50),
    ]

    @pytest.mark.parametrize("f_cr,f_ed,analysis_type,exp_result,exp_uc", testdata)  # noqa: PT006
    def test_evaluation(self, f_cr: float, f_ed: float, analysis_type: Literal["elastic", "plastic"], exp_result: bool, exp_uc: float) -> None:
        """Test the evaluation of the result."""
        form = Form5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)
        assert form == exp_result
        assert form.unity_check == pytest.approx(exp_uc)

    @pytest.mark.parametrize(
        ("f_cr", "f_ed", "analysis_type"),
        [
            (1000000, -100000, "elastic"),  # f_ed is negative
            (-1000000, 100000, "elastic"),  # f_cr is negative
        ],
    )
    def test_error_mismatch_sign(self, f_cr: float, f_ed: float, analysis_type: Literal["elastic", "plastic"]) -> None:
        """Test if correct error is raised when provide arguments with different signs."""
        with pytest.raises(MismatchSignError):
            Form5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)

    @pytest.mark.parametrize(
        ("f_cr", "f_ed", "analysis_type"),
        [
            (1000000, 100000, "invalid_input"),  # analysis_type is not of elastic or plastic
        ],
    )
    def test_type_error_analysis_type(self, f_cr: float, f_ed: float, analysis_type: Literal["elastic", "plastic"]) -> None:
        """Test if correct error is raised when provide wrong type."""
        with pytest.raises(ValueError):
            Form5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type)

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
        analysis_type = "elastic"

        # Create test object
        latex = Form5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed, analysis_type=analysis_type).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert expected == actual[representation], f"{representation} representation failed."
