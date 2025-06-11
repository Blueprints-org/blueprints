"""Testing formula 6.3 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_3 import (
    Form6Dot3MinDeductionAreaStaggeredFastenerHoles,
)
from blueprints.validations import LessOrEqualToZeroError, ListsNotSameLengthError, NegativeValueError


class TestForm6Dot3MinDeductionAreaStaggeredFastenerHoles:
    """Validation for formula 6.3 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t = 10.0
        n = 5.0
        d_0 = 20.0
        s = [50.0, 60.0]
        p = [100.0, 120.0]

        # Object to test
        formula = Form6Dot3MinDeductionAreaStaggeredFastenerHoles(t=t, n=n, d_0=d_0, s=s, p=p)

        # Expected result, manually calculated
        manually_calculated_result = 862.5  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("t", "n", "d_0", "s", "p"),
        [
            (-10.0, 5.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # t is negative
            (10.0, -5.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # n is negative
            (10.0, 5.0, -20.0, [50.0, 60.0], [100.0, 120.0]),  # d_0 is negative
            (10.0, 5.0, 20.0, [-50.0, 60.0], [100.0, 120.0]),  # s has a negative value
            (10.0, 5.0, 20.0, [50.0, 60.0], [-100.0, 120.0]),  # p has a negative value
            (0.0, 5.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # t is zero
            (10.0, 0.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # n is zero
            (10.0, 5.0, 0.0, [50.0, 60.0], [100.0, 120.0]),  # d_0 is zero
            (10.0, 5.0, 20.0, [0.0, 60.0], [100.0, 120.0]),  # s has a zero value
            (10.0, 5.0, 20.0, [50.0, 60.0], [0.0, 120.0]),  # p has a zero value
            (10.0, 5.0, 20.0, [50.0, 60.0], [100.0, 120.0, 10.0]),  # p has a zero value
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t: float, n: float, d_0: float, s: list[float], p: list[float]) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError, ListsNotSameLengthError)):
            Form6Dot3MinDeductionAreaStaggeredFastenerHoles(t=t, n=n, d_0=d_0, s=s, p=p)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_{deduction} = t \left( n \cdot d_0 - \sum \frac{s^2}{4 \cdot p} \right) = "
                r"10.000 \left( 5.000 \cdot 20.000 - \left( \frac{50.000^2}{4 \cdot 100.000} + "
                r"\frac{60.000^2}{4 \cdot 120.000} \right) \right) = 862.500 \ mm^2",
            ),
            ("short", r"A_{deduction} = 862.500 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t = 10.0
        n = 5.0
        d_0 = 20.0
        s = [50.0, 60.0]
        p = [100.0, 120.0]

        # Object to test
        latex = Form6Dot3MinDeductionAreaStaggeredFastenerHoles(t=t, n=n, d_0=d_0, s=s, p=p).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
