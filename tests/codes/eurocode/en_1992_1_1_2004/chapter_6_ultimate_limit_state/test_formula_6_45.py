"""Testing formula 6.45 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_45 import Form6Dot45W1Rectangular
from blueprints.validations import NegativeValueError


class TestForm6Dot45W1Rectangular:
    """Validation for formula 6.45 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_1 = 500.0
        c_2 = 400.0
        d = 200.0

        # Object to test
        formula = Form6Dot45W1Rectangular(c_1=c_1, c_2=c_2, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 1211327.412

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_1", "c_2", "d"),
        [
            (-500.0, 400.0, 200.0),  # c_1 is negative
            (500.0, -400.0, 200.0),  # c_2 is negative
            (500.0, 400.0, -200.0),  # d is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, c_1: float, c_2: float, d: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot45W1Rectangular(c_1=c_1, c_2=c_2, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"W_1 = \frac{c_2^2}{4} + c_1 \cdot c_2 + 4 \cdot c_1 \cdot d + 8 \cdot d^2 + \pi \cdot d \cdot c_2 = "
                r"\frac{400.000^2}{4} + 500.000 \cdot 400.000 + 4 \cdot 500.000 \cdot 200.000 + 8 \cdot 200.000^2 + "
                r"\pi \cdot 200.000 \cdot 400.000 = 1211327.412 \ mm^2",
            ),
            ("short", r"W_1 = 1211327.412 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_1 = 500.0
        c_2 = 400.0
        d = 200.0

        # Object to test
        latex = Form6Dot45W1Rectangular(c_1=c_1, c_2=c_2, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
