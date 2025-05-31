"""Testing formula 7.12 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_12 import Form7Dot12EquivalentDiameter
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot12EquivalentDiameter:
    """Validation for formula 7.12 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_1 = 4
        diam_1 = 16.0
        n_2 = 6
        diam_2 = 20.0

        # Object to test
        formula = Form7Dot12EquivalentDiameter(n_1=n_1, diam_1=diam_1, n_2=n_2, diam_2=diam_2)

        # Expected result, manually calculated
        manually_calculated_result = 18.609  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_1", "diam_1", "n_2", "diam_2"),
        [
            (-4, 16.0, 6, 20.0),  # n_1 is negative
            (4, -16.0, 6, 20.0),  # diam_1 is negative
            (4, 16.0, -6, 20.0),  # n_2 is negative
            (4, 16.0, 6, -20.0),  # diam_2 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_1: float, diam_1: float, n_2: float, diam_2: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot12EquivalentDiameter(n_1=n_1, diam_1=diam_1, n_2=n_2, diam_2=diam_2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"⌀_{eq} = \frac{n_1 \cdot ⌀_1^2 + n_2 \cdot ⌀_2^2}{n_1 \cdot ⌀_1 + n_2 \cdot ⌀_2} = "
                r"\frac{4.000 \cdot 16.000^2 + 6.000 \cdot 20.000^2}{4.000 \cdot 16.000 + 6.000 \cdot 20.000} = 18.609 \ mm",
            ),
            ("short", r"⌀_{eq} = 18.609 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_1 = 4
        diam_1 = 16.0
        n_2 = 6
        diam_2 = 20.0

        # Object to test
        latex = Form7Dot12EquivalentDiameter(n_1=n_1, diam_1=diam_1, n_2=n_2, diam_2=diam_2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
