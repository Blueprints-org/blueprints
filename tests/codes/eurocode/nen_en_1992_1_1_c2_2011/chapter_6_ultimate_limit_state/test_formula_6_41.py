"""Testing formula 6.41 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_6_ultimate_limit_state.formula_6_41 import Form6Dot41W1Rectangular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot41W1Rectangular:
    """Validation for formula 6.41 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_1 = 300.0
        c_2 = 400.0
        d = 500.0

        # Object to test
        formula = Form6Dot41W1Rectangular(c_1=c_1, c_2=c_2, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 5907477.796  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_1", "c_2", "d"),
        [
            (-300.0, 400.0, 500.0),  # c_1 is negative
            (300.0, -400.0, 500.0),  # c_2 is negative
            (300.0, 400.0, -500.0),  # d is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, c_1: float, c_2: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot41W1Rectangular(c_1=c_1, c_2=c_2, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"W_1 = \frac{c_1^2}{2} + c_1 \cdot c_2 + 4 \cdot c_2 \cdot d + 16 \cdot d^2 + 2 \cdot \pi \cdot d \cdot c_1 = "
                r"\frac{300.000^2}{2} + 300.000 \cdot 400.000 + 4 \cdot 400.000 \cdot 500.000 + "
                r"16 \cdot 500.000^2 + 2 \cdot \pi \cdot 500.000 \cdot 300.000 = 5907477.796 mm^2",
            ),
            ("short", r"W_1 = 5907477.796 mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_1 = 300.0
        c_2 = 400.0
        d = 500.0

        # Object to test
        latex = Form6Dot41W1Rectangular(c_1=c_1, c_2=c_2, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
