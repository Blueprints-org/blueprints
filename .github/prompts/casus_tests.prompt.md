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
"""Testing formula 6.10a/bN of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_10abn import
    Form6Dot10abNStrengthReductionFactor
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot10abNStrengthReductionFactor:
    """Validation for formula 6.10a/bN from EN 1992-1-1:2004."""

    def test_evaluation_above_60(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 75.0

        # Object to test
        formula = Form6Dot10abNStrengthReductionFactor(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.525

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_below_60(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 30.0

        # Object to test
        formula = Form6Dot10abNStrengthReductionFactor(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.6

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_1", "c_2", "d"),
        [
            (-300.0, 400.0, 500.0),  # c_1 is negative
            (300.0, -400.0, 500.0),  # c_2 is negative
            (300.0, 400.0, -500.0),  # d is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot10abNStrengthReductionFactor(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                    "complete",
                    r"\nu_{1} = \begin{cases} 0.600 & \text{if } f_{ck} \leq 60 \ MPa \\ \max\left(0.9 - \frac{f_{ck}}{200}, 0.5\right) "
                    r"& \text{if } f_{ck} > 60 \ MPa \end{cases} = "
                    r"\begin{cases} 0.600 & \text{if } 30.0 \leq 60 \ MPa \\ \max\left(0.9 - \frac{30.0}{200}, 0.5\right) "
                    r"& \text{if } 30.0 > 60 \ MPa \end{cases} = 0.600 \ -",
            ),
            (
                    "complete_with_units",
                    r"\nu_{1} = \begin{cases} 0.600 & \text{if } f_{ck} \leq 60 \ MPa \\ \max\left(0.9 - \frac{f_{ck}}{200}, 0.5\right) "
                    r"& \text{if } f_{ck} > 60 \ MPa \end{cases} = "
                    r"\begin{cases} 0.600 & \text{if } 30.0 \ MPa \leq 60 \ MPa \\ \max\left(0.9 - \frac{30.0 \ MPa}{200}, 0.5\right) "
                    r"& \text{if } 30.0 > 60 \ MPa \end{cases} = 0.600 \ -",
            ),
            ("short", r"\nu_{1} = 0.600 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30.0

        # Object to test
        latex = Form6Dot10abNStrengthReductionFactor(f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

```