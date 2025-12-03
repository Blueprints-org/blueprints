"""Testing formula 5.1 of NEN-EN 1993-1-1:2006."""

from typing import ClassVar

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_2006.chapter_5_structural_analysis.formula_5_1 import From5Dot1CriteriumDisregardSecondOrderEffects
from blueprints.validations import MismatchSignError


class TestFrom5Dot1CriteriumDisregardSecondOrderEffects:
    """Validation for formula 5.1 from NEN-EN 1993-1-1:2006."""

    testdata: ClassVar[list[tuple[float, float, bool, float]]] = [
        (1000000, 100000, True, 1),
        (1000000, 110000, False, 1.10),
        (1000000, 50000, True, 0.50),
    ]

    @pytest.mark.parametrize("f_cr,f_ed,exp_result,exp_uc", testdata)  # noqa: PT006
    def test_evaluation(self, f_cr: float, f_ed: float, exp_result: bool, exp_uc: float) -> None:
        """Test the evaluation of the result."""
        form = From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed)
        assert form == exp_result
        assert form.unity_check == pytest.approx(exp_uc)

    @pytest.mark.parametrize(
        ("f_cr", "f_ed"),
        [
            (1000000, -100000),  # f_ed is negative
            (-1000000, 100000),  # f_cr is negative
        ],
    )
    def test_error_mismatch_sign(self, f_cr: float, f_ed: float) -> None:
        """Test if correct error is raised when provide arguments with different signs."""
        with pytest.raises(MismatchSignError):
            From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"CHECK \to \alpha_{cr} = \frac{F_{cr}}{F_{Ed}} \ge 10 \to 10.00 = \frac{1000000.00}{100000.00} \ge 10 \to OK"),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representations of the formula."""
        # Example values
        f_cr = 1000000
        f_ed = 100000

        # Create test object
        latex = From5Dot1CriteriumDisregardSecondOrderEffects(f_cr=f_cr, f_ed=f_ed).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert expected == actual[representation], f"{representation} representation failed."
