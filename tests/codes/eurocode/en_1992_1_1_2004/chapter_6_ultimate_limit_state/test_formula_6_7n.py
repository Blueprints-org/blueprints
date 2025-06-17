"""Testing formula 6.7n of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_7n import Form6Dot7nCheckCotTheta
from blueprints.validations import GreaterThan90Error, NegativeValueError


class TestForm6Dot7nCheckCotTheta:
    """Validation for formula 6.7n from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        theta = 30.0

        # Object to test
        formula = Form6Dot7nCheckCotTheta(theta=theta)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("theta"),
        [
            (-30.0),  # theta is negative
            (95.0),  # theta is greater than 90
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, GreaterThan90Error)):
            Form6Dot7nCheckCotTheta(theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to 1 \leq \cot(\theta) \leq 2.5 \to 1 \leq \cot(30.000) \leq 2.5 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta = 30.0

        # Object to test
        latex = Form6Dot7nCheckCotTheta(theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
