"""Testing formula 8.124 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_124 import (
    Form8Dot124SpreadingAngleTangent,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot124SpreadingAngleTangent:
    """Validation for formula 8.124 from FprEN 1992-1-1:2023."""

    def test_evaluation_narrow_element(self) -> None:
        """Tests the evaluation of the result for a narrow element, where the (1 - a/b) / 2 expression governs."""
        # Example values
        a = 200.0
        b = 500.0
        h = 1000.0

        # Object to test
        formula = Form8Dot124SpreadingAngleTangent(a=a, b=b, h=h)

        # Expected result, manually calculated: (1 - 200 / 500) / 2
        manually_calculated_result = 0.3

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_wide_element(self) -> None:
        """Tests the evaluation of the result for a wide element, where the fixed value of 0,5 governs."""
        # Example values
        a = 200.0
        b = 800.0
        h = 200.0

        # Object to test
        formula = Form8Dot124SpreadingAngleTangent(a=a, b=b, h=h)

        # Expected result, as printed in the standard for the wide element case
        manually_calculated_result = 0.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "b", "h"),
        [
            (-200.0, 500.0, 1000.0),  # a is negative
            (200.0, 500.0, -1000.0),  # h is negative
        ],
    )
    def test_raise_error_when_a_or_h_is_negative(self, a: float, b: float, h: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot124SpreadingAngleTangent(a=a, b=b, h=h)

    @pytest.mark.parametrize(
        "b",
        [
            -500.0,  # b is negative
            0.0,  # b is zero
        ],
    )
    def test_raise_error_when_b_is_less_or_equal_to_zero(self, b: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot124SpreadingAngleTangent(a=200.0, b=b, h=1000.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tan\theta_{cf} = \begin{cases} \dfrac{1 - a/b}{2} & \text{if } b \leq a + H/2 \\ "
                    r"0.5 & \text{if } b > a + H/2 \end{cases} = "
                    r"\begin{cases} \dfrac{1 - 200.000/500.000}{2} & \text{if } 500.000 \leq 200.000 + 1000.000/2 \\ "
                    r"0.5 & \text{if } 500.000 > 200.000 + 1000.000/2 \end{cases} = 0.300 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tan\theta_{cf} = \begin{cases} \dfrac{1 - a/b}{2} & \text{if } b \leq a + H/2 \\ "
                    r"0.5 & \text{if } b > a + H/2 \end{cases} = "
                    r"\begin{cases} \dfrac{1 - 200.000/500.000}{2} & \text{if } 500.000 \leq 200.000 + 1000.000/2 \\ "
                    r"0.5 & \text{if } 500.000 > 200.000 + 1000.000/2 \end{cases} = 0.300 \ -"
                ),
            ),
            ("short", r"\tan\theta_{cf} = 0.300 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 200.0
        b = 500.0
        h = 1000.0

        # Object to test
        latex = Form8Dot124SpreadingAngleTangent(a=a, b=b, h=h).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
