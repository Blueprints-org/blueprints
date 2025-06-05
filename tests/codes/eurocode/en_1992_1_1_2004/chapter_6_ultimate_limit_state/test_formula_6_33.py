"""Testing formula 6.33 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_33 import Form6Dot33ContourRadiusCircularColumnHeads
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot33ContourRadiusCircularColumnHeads:
    """Validation for formula 6.33 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d = 500.0
        l_h = 1000.0
        c = 300.0

        # Object to test
        formula = Form6Dot33ContourRadiusCircularColumnHeads(d=d, l_h=l_h, c=c)

        # Expected result, manually calculated
        manually_calculated_result = 2150.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d", "l_h", "c"),
        [
            (-500.0, 1000.0, 300.0),  # d is negative
            (500.0, -1000.0, 300.0),  # l_h is negative
            (500.0, 1000.0, -300.0),  # c is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d: float, l_h: float, c: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot33ContourRadiusCircularColumnHeads(d=d, l_h=l_h, c=c)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"r_{cont} = 2 \cdot d + l_{H} + 0.5 \cdot c = 2 \cdot 500.000 + 1000.000 + 0.5 \cdot 300.000 = 2150.000 \ mm",
            ),
            ("short", r"r_{cont} = 2150.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 500.0
        l_h = 1000.0
        c = 300.0

        # Object to test
        latex = Form6Dot33ContourRadiusCircularColumnHeads(d=d, l_h=l_h, c=c).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
