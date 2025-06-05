"""Testing formula 6.26 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_26 import Form6Dot26ShearStressInWall
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot26ShearStressInWall:
    """Validation for formula 6.26 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t_ed = 100.0
        a_k = 200.0

        # Object to test
        formula = Form6Dot26ShearStressInWall(t_ed=t_ed, a_k=a_k)

        # Expected result, manually calculated
        manually_calculated_result = 0.25  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("t_ed", "a_k"),
        [
            (-100.0, 200.0),  # t_ed is negative
            (100.0, -200.0),  # a_k is negative
            (100.0, 0.0),  # a_k is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t_ed: float, a_k: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot26ShearStressInWall(t_ed=t_ed, a_k=a_k)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{t,i}t_{ef,i} = \frac{T_{Ed}}{2 \cdot A_{k}} = \frac{100.000}{2 \cdot 200.000} = 0.250 \ N/mm",
            ),
            ("short", r"\tau_{t,i}t_{ef,i} = 0.250 \ N/mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t_ed = 100.0
        a_k = 200.0

        # Object to test
        latex = Form6Dot26ShearStressInWall(t_ed=t_ed, a_k=a_k).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
