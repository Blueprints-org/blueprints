"""Testing formula 5.7 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_5_structural_analysis.formula_5_7 import Form5Dot7DisregardFrameSwayImperfections
from blueprints.validations import NegativeValueError


class TestForm5Dot8NeglectFrameTilt:
    """Validation for formula 5.7 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        h_ed = 50000
        v_ed = 100000

        # Create test object
        form = Form5Dot7DisregardFrameSwayImperfections(h_ed=h_ed, v_ed=v_ed)

        # Expected results
        exp_result = True
        exp_uc = h_ed / (0.15 * v_ed)

        # Test
        assert form == exp_result
        assert form.unity_check == exp_uc

    @pytest.mark.parametrize(
        ("h_ed", "v_ed"),
        [
            (50000, -100000),  # v_ed is negative
            (-50000, 100000),  # h_ed is negative
        ],
    )
    def test_error_when_negative(self, h_ed: float, v_ed: float) -> None:
        """Test if correct error is raised when provide negatives or zeroes."""
        with pytest.raises(NegativeValueError):
            Form5Dot7DisregardFrameSwayImperfections(v_ed=v_ed, h_ed=h_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"CHECK \to H_{Ed} \geq 0.15 \cdot V_{Ed} \to 50000.00 \geq 0.15 \cdot 100000.00 \to OK"),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representations of the formula."""
        # Example values
        h_ed = 50000
        v_ed = 100000

        # Create test object
        latex = Form5Dot7DisregardFrameSwayImperfections(h_ed=h_ed, v_ed=v_ed).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert expected == actual[representation], f"{representation} representation failed ."
