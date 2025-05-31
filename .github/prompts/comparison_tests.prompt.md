## Code notes

- Write tests for all classes found in the linked file. All should be in the format as is presented in the current template. 
- The manually calculated results should just be presented as a bool. 
- Keep all formatting and naming conventions such as they currently are. Public docstring on top. Then pytest import. Then project imports. Then classes.
- The latex formula always has 3 decimals. 
- Write one test with succesful input, that retuns the answer of the equation. 
- For all variables found in the raise_if_negative of the linked formula, write a test where its input is given as a negative value.
- For all variables found in the raise_if_less_or_equal_to_zero of the linked formula, write a test where its input is given as zero and a test where its given as a negative value.
- For the LaTeX complete and short presentation, make sure you add a unit at the end. For the complete_with_units, add units to all variables except for those that are dimensionless

## Template for service

```python
"""Testing formula 5.38a of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_38a import
    Form5Dot38aCheckRelativeSlendernessRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot38aCheckRelativeSlendernessRatio:
    """Validation for formula 5.38a from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        length_y = 1.0
        length_z = 1.5

        # Object to test
        formula = Form5Dot38aCheckRelativeSlendernessRatio(length_y=length_y, length_z=length_z)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("length_y", "length_z"),
        [
            (-1.0, 1.5),  # length_y is negative
            (1.0, -1.5),  # length_z is negative
            (0.0, 1.5),  # length_y is zero
            (1.0, 0.0),  # length_z is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, length_y: float, length_z: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot38aCheckRelativeSlendernessRatio(length_y=length_y, length_z=length_z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                    "complete",
                    r"CHECK \to \left( \frac{L_{y}}{L_{z}} \leq 2 \text{ and } \frac{L_{z}}{L_{y}} \leq 2 \right) \to "
                    r"\left( \frac{1.000}{1.500} \leq 2 \text{ and } \frac{1.500}{1.000} \leq 2 \right) \to OK",
            ),
            (
                    "complete_with_units",
                    r"CHECK \to \left( \frac{L_{y}}{L_{z}} \leq 2 \text{ and } \frac{L_{z}}{L_{y}} \leq 2 \right) \to "
                    r"\left( \frac{1.000 \ mm}{1.500 \ mm} \leq 2 \text{ and } \frac{1.500 \ mm}{1.000 \ mm} "
                    r"\leq 2 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        length_y = 1.0
        length_z = 1.5

        # Object to test
        latex = Form5Dot38aCheckRelativeSlendernessRatio(length_y=length_y, length_z=length_z).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

```