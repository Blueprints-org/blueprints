"""Testing formula 8.129 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_129 import (
    Form8Dot129ContributingConcreteArea,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot129ContributingConcreteArea:
    """Validation for formula 8.129 from FprEN 1992-1-1:2023."""

    def test_evaluation_expression_governs(self) -> None:
        """Tests the evaluation of the result where the b0 + (a - a0) expression governs."""
        # Example values
        a = 500.0
        a_0 = 450.0
        b_0 = 100.0
        b = 1000.0

        # Object to test
        formula = Form8Dot129ContributingConcreteArea(a=a, a_0=a_0, b_0=b_0, b=b)

        # Expected result, manually calculated: 500 * min(100 + (500 - 450), 1000) = 500 * 150
        manually_calculated_result = 75000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_bound_governs(self) -> None:
        """Tests the evaluation of the result where the bound b governs."""
        # Example values
        a = 500.0
        a_0 = 200.0
        b_0 = 100.0
        b = 350.0

        # Object to test
        formula = Form8Dot129ContributingConcreteArea(a=a, a_0=a_0, b_0=b_0, b=b)

        # Expected result, manually calculated: 500 * min(100 + (500 - 200), 350) = 500 * 350
        manually_calculated_result = 175000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "a_0", "b_0", "b"),
        [
            (-500.0, 300.0, 400.0, 600.0),  # a is negative
            (500.0, -300.0, 400.0, 600.0),  # a_0 is negative
            (500.0, 300.0, -400.0, 600.0),  # b_0 is negative
            (500.0, 300.0, 400.0, -600.0),  # b is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, a_0: float, b_0: float, b: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot129ContributingConcreteArea(a=a, a_0=a_0, b_0=b_0, b=b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"A_{c1} = a \cdot \min\left(b_0 + \left(a - a_0\right), b\right) = "
                    r"500.000 \cdot \min\left(400.000 + \left(500.000 - 300.000\right), 600.000\right) = 300000.000 \ mm^2"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"A_{c1} = a \cdot \min\left(b_0 + \left(a - a_0\right), b\right) = "
                    r"500.000 \ mm \cdot \min\left(400.000 \ mm + \left(500.000 \ mm - 300.000 \ mm\right), 600.000 \ mm\right) = "
                    r"300000.000 \ mm^2"
                ),
            ),
            ("short", r"A_{c1} = 300000.000 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 500.0
        a_0 = 300.0
        b_0 = 400.0
        b = 600.0

        # Object to test
        latex = Form8Dot129ContributingConcreteArea(a=a, a_0=a_0, b_0=b_0, b=b).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
