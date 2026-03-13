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
"""Testing formula 5.17 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_17 import Form5Dot17CompressionCheckZProfilesClass1And2
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot17CompressionCheckZProfilesClass1And2:
    """Validation for formula 5.17 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 12.0  # kN
        n_pl_rd = 200.0  # kN

        # Object to test
        formula = Form5Dot17CompressionCheckZProfilesClass1And2(n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result
        assert formula.unity_check == n_ed / n_pl_rd

    @pytest.mark.parametrize(
        ("n_ed", "n_pl_rd"),
        [
            (50.0, 0.0),  # n_pl_rd is zero
            (50.0, -100.0),  # n_pl_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, n_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot17CompressionCheckZProfilesClass1And2(n_ed=n_ed, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{N_{Ed}}{N_{pl,Rd}} \leq 0.1 \to \frac{12.000}{200.000} \leq 0.1 \to \frac 0.06 \leq 0.1 \to OK",
            ),
            ("short", r"CHECK \to OK"),
            ("complete_with_units", r"CHECK \to \frac{N_{Ed}}{N_{pl,Rd}} \leq 0.1 \to \frac{12.000 \ kN}{200.000 \ kN} \leq 0.1 \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 12.0  # kN
        n_pl_rd = 200.0  # kN

        # Object to test
        latex = Form5Dot17CompressionCheckZProfilesClass1And2(n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


```