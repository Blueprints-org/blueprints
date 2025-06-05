"""Testing formula 9.7N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_7n import Form9Dot7nMaximumDistanceBentUpBars
from blueprints.validations import GreaterThan90Error, NegativeValueError


class TestForm9Dot7nMaximumDistanceBentUpBars:
    """Validation for formula 9.7N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg
        form_9_7n = Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 65.24931981

        assert form_9_7n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is raised when d is negative."""
        d = -100  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test if error is raised when alpha is negative."""
        d = 100  # mm
        alpha = -85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

    def test_raise_error_when_alpha_is_greater_90(self) -> None:
        """Test if error is raised when alpha is negative."""
        d = 100  # mm
        alpha = 110  # deg

        with pytest.raises(GreaterThan90Error):
            Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{b,max} = 0.6 \cdot d \cdot \left( 1 + cot(\alpha) \right) = 0.6 \cdot 100.00 \cdot \left( 1 + cot(85.00) \right) = 65.25",
            ),
            ("short", r"s_{b,max} = 65.25"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg

        # Object to test
        form_9_7n_latex = Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha).latex()

        actual = {"complete": form_9_7n_latex.complete, "short": form_9_7n_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
