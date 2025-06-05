"""Testing formula 9.10 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_10 import Form9Dot10MaximumSpacingBentUpBars
from blueprints.validations import NegativeValueError


class TestForm9Dot10MaximumSpacingBentUpBars:
    """Validation for formula 9.10 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 200  # mm
        form_9_10 = Form9Dot10MaximumSpacingBentUpBars(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 200

        assert form_9_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is given when d is negative."""
        d = -200  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot10MaximumSpacingBentUpBars(d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{max} = d = 100.00 = 100.00",
            ),
            ("short", r"s_{max} = 100.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 100  # mm

        # Object to test
        form_9_10_latex = Form9Dot10MaximumSpacingBentUpBars(d=d).latex()

        actual = {"complete": form_9_10_latex.complete, "short": form_9_10_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
