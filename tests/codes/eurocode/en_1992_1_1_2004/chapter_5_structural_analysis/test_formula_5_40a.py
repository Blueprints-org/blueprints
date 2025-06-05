"""Testing formula 5.40a of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_40a import Form5Dot40aCheckLateralInstability
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot40aCheckLateralInstability:
    """Validation for formula 5.40a from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        l_0t = 6.0  # m
        b = 0.3  # m
        h = 0.5  # m

        # Object to test
        formula = Form5Dot40aCheckLateralInstability(l_0t=l_0t, b=b, h=h)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("l_0t", "b", "h"),
        [
            (-6.0, 0.3, 0.5),  # l_0t is negative
            (6.0, -0.3, 0.5),  # b is negative
            (6.0, 0.3, -0.5),  # h is negative
            (6.0, 0.0, 0.5),  # b is zero
            (6.0, 0.3, 0.0),  # h is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, l_0t: float, b: float, h: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot40aCheckLateralInstability(l_0t=l_0t, b=b, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{l_{0t}}{b} \leq \frac{50}{\left( h/b \right)^{1/3}} \text{ and } \frac{h}{b} \leq 2.5 \right) \to "
                r"\left( \frac{6.000}{0.300} \leq \frac{50}{\left( 0.500/0.300 \right)^{1/3}} \text{ and } "
                r"\frac{0.500}{0.300} \leq 2.5 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_0t = 6.0  # m
        b = 0.3  # m
        h = 0.5  # m

        # Object to test
        latex = Form5Dot40aCheckLateralInstability(l_0t=l_0t, b=b, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
