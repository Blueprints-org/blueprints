"""Testing formula 4.3N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.formula_4_3n import Form4Dot3nCheckExecutionTolerances
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm4Dot3nCheckExecutionTolerances:
    """Validation for formula 4.3N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        delta_cdev = 7.0

        # Object to test
        formula = Form4Dot3nCheckExecutionTolerances(delta_cdev=delta_cdev)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("delta_cdev"),
        [
            (-1.0),  # delta_cdev
            (0.0),  # delta_cdev is 0
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, delta_cdev: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form4Dot3nCheckExecutionTolerances(delta_cdev=delta_cdev)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to 5 \leq \Delta c_{dev} \leq 10 \to 5 \leq 7.000 \leq 10 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        delta_cdev = 7.0

        # Object to test
        latex = Form4Dot3nCheckExecutionTolerances(delta_cdev=delta_cdev).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
