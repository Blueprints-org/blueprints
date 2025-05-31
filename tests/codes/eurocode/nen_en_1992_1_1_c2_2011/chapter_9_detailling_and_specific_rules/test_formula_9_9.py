"""Testing formula 9.9 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_9 import Form9Dot9MaximumSpacingSeriesOfLinks
from blueprints.validations import NegativeValueError


class TestForm9Dot9MaximumSpacingSeriesOfLinks:
    """Validation for formula 9.9 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg
        form_9_9 = Form9Dot9MaximumSpacingSeriesOfLinks(d=d, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 81.56164976

        assert form_9_9 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is given when d is negative."""
        d = -100  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot9MaximumSpacingSeriesOfLinks(d=d, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{max} = 0.75 \cdot d \cdot \left( 1 + cot(\alpha) \right) = 0.75 \cdot 100.00 \cdot \left( 1 + cot(85.00) \right) = 81.56",
            ),
            ("short", r"s_{max} = 81.56"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg

        # Object to test
        form_9_9n_latex = Form9Dot9MaximumSpacingSeriesOfLinks(d=d, alpha=alpha).latex()

        actual = {"complete": form_9_9n_latex.complete, "short": form_9_9n_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
