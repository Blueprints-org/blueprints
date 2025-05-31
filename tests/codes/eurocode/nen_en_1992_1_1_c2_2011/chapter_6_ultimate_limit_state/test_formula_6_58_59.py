"""Testing formula 6.58/6.59 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_58_59 import Form6Dot58And59TensileForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot58And59TensileForce:
    """Validation for formula 6.58/6.59 from EN 1992-1-1:2004."""

    def test_evaluation58(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f = 500.0
        a = 50.0
        b = 100.0
        capital_h = 400.0

        # Object to test
        formula = Form6Dot58And59TensileForce(f=f, a=a, b=b, capital_h=capital_h)

        # Expected result, manually calculated
        manually_calculated_result = 62.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation59(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f = 500.0
        a = 200.0
        b = 300.0
        capital_h = 400.0

        # Object to test
        formula = Form6Dot58And59TensileForce(f=f, a=a, b=b, capital_h=capital_h)

        # Expected result, manually calculated
        manually_calculated_result = 37.500

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f", "a", "b", "capital_h"),
        [
            (-500.0, 200.0, 300.0, 400.0),  # f is negative
            (500.0, -200.0, 300.0, 400.0),  # a is negative
            (500.0, 200.0, -300.0, 400.0),  # b is negative
            (500.0, 200.0, 300.0, -400.0),  # capital_h is negative
            (500.0, 200.0, 0.0, 400.0),  # b is zero
            (500.0, 200.0, 300.0, 0.0),  # capital_h is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f: float, a: float, b: float, capital_h: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot58And59TensileForce(f=f, a=a, b=b, capital_h=capital_h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"T = \begin{cases} \frac{1}{4} \cdot \frac{ b - a}{ b} \cdot F & \text{if } b \leq \frac{H}{2} \\ "
                r"\frac{1}{4} \cdot \left(1 - 0.7 \cdot \frac{ a}{\frac{H}{2}}\right) \cdot F & \text{if } b > \frac{H}{2} \end{cases}"
                r" = \begin{cases} \frac{1}{4} \cdot \frac{ 300.000 - 200.000}{ 300.000} \cdot 500.000 & \text{if } 300.000 "
                r"\leq \frac{400.000}{2} \\ \frac{1}{4} \cdot \left(1 - 0.7 \cdot \frac{ 200.000}{\frac{400.000}{2}}\right) \cdot "
                r"500.000 & \text{if } 300.000 > \frac{400.000}{2} \end{cases} = 37.500 \ N",
            ),
            ("short", r"T = 37.500 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f = 500.0
        a = 200.0
        b = 300.0
        capital_h = 400.0

        # Object to test
        latex = Form6Dot58And59TensileForce(f=f, a=a, b=b, capital_h=capital_h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
