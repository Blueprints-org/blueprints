"""Testing formula 3.13 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_13 import Form3Dot13CoefficientTimeAutogeneShrinkage


class TestForm3Dot13CoefficientTimeAutogeneShrinkage:
    """Validation for formula 3.13 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        t = 5  # days
        form_3_13 = Form3Dot13CoefficientTimeAutogeneShrinkage(t=t)

        # Expected result, manually calculated
        manually_calculated_result = 0.3605927

        assert form_3_13 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        t = -5  # days

        with pytest.raises(ValueError):
            Form3Dot13CoefficientTimeAutogeneShrinkage(t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta_{as}(t) = 1 - \exp(-0.2 \cdot t^{0.5}) = 1 - \exp(-0.2 \cdot 5.00^{0.5}) = 0.36",
            ),
            ("short", r"\beta_{as}(t) = 0.36"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t = 5  # days

        # Object to test
        form_3_13_latex = Form3Dot13CoefficientTimeAutogeneShrinkage(t=t).latex()

        actual = {"complete": form_3_13_latex.complete, "short": form_3_13_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
