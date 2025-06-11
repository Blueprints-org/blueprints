"""Testing formula 6.39aw of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_39aw import (
    Form6Dot39awHollowSections,
    Form6Dot39awWeldedBoxSections,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot39awHollowSections:
    """Validation for formula 6.39aw (hollow sections) from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 7000.0  # updated default value
        b = 200.0
        t = 10.0

        formula = Form6Dot39awHollowSections(a=a, b=b, t=t)
        manually_calculated_result = 0.42857142857  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "t"),
        [
            (-7000.0, 200.0, 10.0),  # a is negative
            (7000.0, -200.0, 10.0),  # b is negative
            (7000.0, 200.0, -10.0),  # t is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot39awHollowSections(a=a, b=b, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_w = \min \left( \frac{A - 2 \cdot b \cdot t}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 - 2 \cdot 200.000 \cdot 10.000}{7000.000}, 0.5 \right) = 0.429 \ -",
            ),
            (
                "complete_with_units",
                r"a_w = \min \left( \frac{A - 2 \cdot b \cdot t}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 \ mm^2 - 2 \cdot 200.000 \ mm \cdot 10.000 \ mm}"
                r"{7000.000 \ mm^2}, 0.5 \right) = 0.429 \ -",
            ),
            ("short", r"a_w = 0.429 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 7000.0  # updated default value
        b = 200.0
        t = 10.0

        latex = Form6Dot39awHollowSections(a=a, b=b, t=t).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot39awWeldedBoxSections:
    """Validation for formula 6.39aw (welded box sections) from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 7000.0  # updated default value
        b = 200.0
        t_f = 10.0

        formula = Form6Dot39awWeldedBoxSections(a=a, b=b, t_f=t_f)
        manually_calculated_result = 0.42857142857  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "t_f"),
        [
            (-7000.0, 200.0, 10.0),  # a is negative
            (7000.0, -200.0, 10.0),  # b is negative
            (7000.0, 200.0, -10.0),  # t_f is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, b: float, t_f: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot39awWeldedBoxSections(a=a, b=b, t_f=t_f)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_w = \min \left( \frac{A - 2 \cdot b \cdot t_f}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 - 2 \cdot 200.000 \cdot 10.000}{7000.000}, 0.5 \right) = 0.429 \ -",
            ),
            (
                "complete_with_units",
                r"a_w = \min \left( \frac{A - 2 \cdot b \cdot t_f}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 \ mm^2 - 2 \cdot 200.000 \ mm \cdot 10.000 \ mm}"
                r"{7000.000 \ mm^2}, 0.5 \right) = 0.429 \ -",
            ),
            ("short", r"a_w = 0.429 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 7000.0  # updated default value
        b = 200.0
        t_f = 10.0

        latex = Form6Dot39awWeldedBoxSections(a=a, b=b, t_f=t_f).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
