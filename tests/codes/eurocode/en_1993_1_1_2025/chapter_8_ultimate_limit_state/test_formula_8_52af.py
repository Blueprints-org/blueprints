"""Testing formula 8.52af from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_52af import (
    Form8Dot52afHollowSections,
    Form8Dot52afWeldedBoxSections,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot52afHollowSections:
    """Validation for formula 8.52af (hollow sections) from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 7000.0  # updated default value
        h = 300.0
        t = 10.0

        formula = Form8Dot52afHollowSections(a=a, h=h, t=t)
        manually_calculated_result = 0.14285714285  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "h", "t"),
        [
            (-7000.0, 300.0, 10.0),  # a is negative
            (7000.0, -300.0, 10.0),  # h is negative
            (7000.0, 300.0, -10.0),  # t is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, h: float, t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot52afHollowSections(a=a, h=h, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_f = \min \left( \frac{A - 2 \cdot h \cdot t}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 - 2 \cdot 300.000 \cdot 10.000}{7000.000}, 0.5 \right) = 0.143 \ -",
            ),
            (
                "complete_with_units",
                r"a_f = \min \left( \frac{A - 2 \cdot h \cdot t}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 \ mm^2 - 2 \cdot 300.000 \ mm \cdot 10.000 \ mm}"
                r"{7000.000 \ mm^2}, 0.5 \right) = 0.143 \ -",
            ),
            ("short", r"a_f = 0.143 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 7000.0  # updated default value
        h = 300.0
        t = 10.0

        latex = Form8Dot52afHollowSections(a=a, h=h, t=t).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm8Dot52afWeldedBoxSections:
    """Validation for formula 8.52af (welded box sections) from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        a = 7000.0  # updated default value
        h = 300.0
        t_w = 10.0

        formula = Form8Dot52afWeldedBoxSections(a=a, h=h, t_w=t_w)
        manually_calculated_result = 0.14285714285  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "h", "t_w"),
        [
            (-7000.0, 300.0, 10.0),  # a is negative
            (7000.0, -300.0, 10.0),  # h is negative
            (7000.0, 300.0, -10.0),  # t_w is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, h: float, t_w: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot52afWeldedBoxSections(a=a, h=h, t_w=t_w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_f = \min \left( \frac{A - 2 \cdot h \cdot t_w}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 - 2 \cdot 300.000 \cdot 10.000}{7000.000}, 0.5 \right) = 0.143 \ -",
            ),
            (
                "complete_with_units",
                r"a_f = \min \left( \frac{A - 2 \cdot h \cdot t_w}{A}, 0.5 \right) = "
                r"\min \left( \frac{7000.000 \ mm^2 - 2 \cdot 300.000 \ mm \cdot 10.000 \ mm}"
                r"{7000.000 \ mm^2}, 0.5 \right) = 0.143 \ -",
            ),
            ("short", r"a_f = 0.143 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        a = 7000.0  # updated default value
        h = 300.0
        t_w = 10.0

        latex = Form8Dot52afWeldedBoxSections(a=a, h=h, t_w=t_w).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
