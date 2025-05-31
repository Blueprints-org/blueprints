## Code notes

- Write tests for all classes found in the linked file. All should be in the format as is presented in the current template. 
- The manually calculated results should just be presented as floats. 
- Keep all formatting and naming conventions such as they currently are. Public docstring on top. Then pytest import. Then project imports. Then classes.
- The latex formula always has 3 decimals. 
- Write one test with succesful input, that retuns the answer of the equation. 
- For all variables found in the raise_if_negative of the linked formula, write a test where its input is given as a negative value.
- For all variables found in the raise_if_less_or_equal_to_zero of the linked formula, write a test where its input is given as zero and a test where its given as a negative value.
- For the LaTeX complete and short presentation, make sure you add a unit at the end. For the complete_with_units, add units to all variables except for those that are dimensionless

## Template for service

```python
"""Testing formula 6.41 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_41 import
    Form6Dot41W1Rectangular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot41W1Rectangular:
    """Validation for formula 6.41 from EN 1992-1-1:2004."""

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
                    r"W_1 = \frac{(c_1)^2}{2} + c_1 \cdot c_2 + 4 \cdot c_2 \cdot d + 16 \cdot (d)^2 + 2 \cdot \pi \cdot d \cdot c_1 = "
                    r"\frac{(300.000)^2}{2} + 300.000 \cdot 400.000 + 4 \cdot 400.000 \cdot 500.000 + "
                    r"16 \cdot (500.000)^2 + 2 \cdot \pi \cdot 500.000 \cdot 300.000 = 5907477.796 \ mm^2",
            ),
            (
                    "complete_with_units",
                    r"W_1 = \frac{(c_1)^2}{2} + c_1 \cdot c_2 + 4 \cdot c_2 \cdot d + 16 \cdot (d)^2 + 2 \cdot \pi \cdot d \cdot c_1 = "
                    r"\frac{(300.000 \ mm)^2}{2} + 300.000 \ mm \cdot 400.000 \ mm + 4 \cdot 400.000 \ mm \cdot 500.000 \ mm + "
                    r"16 \cdot (500.000 \ mm)^2 + 2 \cdot \pi \cdot 500.000 \ mm \cdot 300.000 \ mm = 5907477.796 \ mm^2",
            ),
            ("short", r"W_1 = 5907477.796 \ mm^2"),
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

```