"""Testing formula 9.8N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_8n import (
    Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks:
    """Validation for formula 9.8N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 500  # mm
        form_9_8n = Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 375

        assert form_9_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_maximum_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 1000  # mm
        form_9_8n = Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 600

        assert form_9_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is raised when d is negative."""
        d = -100  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks(d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{t,max} = min(0.75 \cdot d, 600 \text{mm}) = min(0.75 \cdot 500.00, 600 \text{mm}) = 375.00",
            ),
            ("short", r"s_{t,max} = 375.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        d = 500  # mm

        # Object to test
        form_9_8n_latex = Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks(d=d).latex()

        actual = {"complete": form_9_8n_latex.complete, "short": form_9_8n_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
