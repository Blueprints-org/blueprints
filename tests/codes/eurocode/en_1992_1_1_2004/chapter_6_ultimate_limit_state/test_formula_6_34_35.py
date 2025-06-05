"""Testing formulas 6.34 and 6.35 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_34_35 import Form6Dot34And35ContourRadiusRectangular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot34And35ContourRadiusRectangular:
    """Validation for formulas 6.34 and 6.35 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d = 500.0
        c_1 = 300.0
        c_2 = 400.0
        l_h1 = 600.0
        l_h2 = 800.0

        # Object to test
        formula = Form6Dot34And35ContourRadiusRectangular(d=d, c_1=c_1, c_2=c_2, l_h1=l_h1, l_h2=l_h2)

        # Expected result, manually calculated
        manually_calculated_result = 1969.94845224  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_reversed_values(self) -> None:
        """Tests the evaluation of the result with reversed values."""
        # Example values
        d = 500.0
        c_1 = 400.0
        c_2 = 300.0
        l_h1 = 800.0
        l_h2 = 600.0

        # Object to test
        formula = Form6Dot34And35ContourRadiusRectangular(d=d, c_1=c_1, c_2=c_2, l_h1=l_h1, l_h2=l_h2)

        # Expected result, manually calculated
        manually_calculated_result = 1969.94845224  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d", "c_1", "c_2", "l_h1", "l_h2"),
        [
            (-500.0, 300.0, 400.0, 600.0, 800.0),  # d is negative
            (500.0, -300.0, 400.0, 600.0, 800.0),  # c_1 is negative
            (500.0, 300.0, -400.0, 600.0, 800.0),  # c_2 is negative
            (500.0, 300.0, 400.0, -600.0, 800.0),  # l_h1 is negative
            (500.0, 300.0, 400.0, 600.0, -800.0),  # l_h2 is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d: float, c_1: float, c_2: float, l_h1: float, l_h2: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot34And35ContourRadiusRectangular(d=d, c_1=c_1, c_2=c_2, l_h1=l_h1, l_h2=l_h2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"r_{cont} = min\left(2 \cdot d + 0.56 \cdot \sqrt{(c_1 + 2 \cdot l_{H1}) \cdot (c_2 + 2 \cdot l_{H2})}, "
                r"2 \cdot d + 0.69 \cdot (c_1 + 2 \cdot l_{H1})\right)"
                r" = min\left(2 \cdot 500.000 + 0.56 \cdot \sqrt{(300.000 + 2 \cdot 600.000) \cdot (400.000 + 2 \cdot 800.000)}, "
                r"2 \cdot 500.000 + 0.69 \cdot (300.000 + 2 \cdot 600.000)\right) = 1969.948 \ mm",
            ),
            ("short", r"r_{cont} = 1969.948 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 500.0
        c_1 = 300.0
        c_2 = 400.0
        l_h1 = 600.0
        l_h2 = 800.0

        # Object to test
        latex = Form6Dot34And35ContourRadiusRectangular(d=d, c_1=c_1, c_2=c_2, l_h1=l_h1, l_h2=l_h2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"r_{cont} = min\left(2 \cdot d + 0.56 \cdot \sqrt{(c_1 + 2 \cdot l_{H1}) \cdot (c_2 + 2 \cdot l_{H2})}, "
                r"2 \cdot d + 0.69 \cdot (c_1 + 2 \cdot l_{H1})\right)"
                r" = min\left(2 \cdot 500.000 + 0.56 \cdot \sqrt{(300.000 + 2 \cdot 600.000) \cdot (400.000 + 2 \cdot 800.000)}, "
                r"2 \cdot 500.000 + 0.69 \cdot (300.000 + 2 \cdot 600.000)\right) = 1969.948 \ mm",
            ),
            ("short", r"r_{cont} = 1969.948 \ mm"),
        ],
    )
    def test_latex_reversed_values(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula with reversed values."""
        # Example values
        d = 500.0
        c_1 = 400.0
        c_2 = 300.0
        l_h1 = 800.0
        l_h2 = 600.0

        # Object to test
        latex = Form6Dot34And35ContourRadiusRectangular(d=d, c_1=c_1, c_2=c_2, l_h1=l_h1, l_h2=l_h2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
