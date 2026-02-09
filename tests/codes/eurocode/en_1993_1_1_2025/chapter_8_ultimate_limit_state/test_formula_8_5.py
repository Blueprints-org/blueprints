"""Testing formula 8.5 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_5 import (
    Form8Dot5MinDeductionAreaStaggeredFastenerHoles,
)
from blueprints.validations import LessOrEqualToZeroError, ListsNotSameLengthError, NegativeValueError


class TestForm8Dot5MinDeductionAreaStaggeredFastenerHoles:
    """Validation for formula 8.5 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values

        t = 10.0
        n1 = 5.0
        d_0 = 20.0
        s = [50.0, 60.0]
        p2 = [100.0, 120.0]

        # Object to test
        formula = Form8Dot5MinDeductionAreaStaggeredFastenerHoles(t=t, n_1=n1, d_0=d_0, s=s, p_2=p2)

        # Expected result, manually calculated
        manually_calculated_result = 862.5  # mm^2

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("t", "n1", "d_0", "s", "p2"),
        [
            (-10.0, 5.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # t is negative
            (10.0, -5.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # n1 is negative
            (10.0, 5.0, -20.0, [50.0, 60.0], [100.0, 120.0]),  # d_0 is negative
            (10.0, 5.0, 20.0, [-50.0, 60.0], [100.0, 120.0]),  # s has a negative value
            (10.0, 5.0, 20.0, [50.0, 60.0], [-100.0, 120.0]),  # p2 has a negative value
            (0.0, 5.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # t is zero
            (10.0, 0.0, 20.0, [50.0, 60.0], [100.0, 120.0]),  # n1 is zero
            (10.0, 5.0, 0.0, [50.0, 60.0], [100.0, 120.0]),  # d_0 is zero
            (10.0, 5.0, 20.0, [0.0, 60.0], [100.0, 120.0]),  # s has a zero value
            (10.0, 5.0, 20.0, [50.0, 60.0], [0.0, 120.0]),  # p2 has a zero value
            (10.0, 5.0, 20.0, [50.0, 60.0], [100.0, 120.0, 10.0]),  # p2 has a zero value
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t: float, n1: float, d_0: float, s: list[float], p2: list[float]) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError, ListsNotSameLengthError)):
            Form8Dot5MinDeductionAreaStaggeredFastenerHoles(t=t, n_1=n1, d_0=d_0, s=s, p_2=p2)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta A_{net,1} = t \left( n_1 \cdot d_0 - \sum \frac{s^2}{4 \cdot p_2} \right) = "
                r"10.000 \left( 5.000 \cdot 20.000 - \left( \frac{50.000^2}{4 \cdot 100.000} + "
                r"\frac{60.000^2}{4 \cdot 120.000} \right) \right) = 862.500 \ mm^2",
            ),
            ("short", r"\Delta A_{net,1} = 862.500 \ mm^2"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t = 10.0
        n1 = 5.0
        d_0 = 20.0
        s = [50.0, 60.0]
        p2 = [100.0, 120.0]

        # Object to test
        latex = Form8Dot5MinDeductionAreaStaggeredFastenerHoles(t=t, n_1=n1, d_0=d_0, s=s, p_2=p2).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
