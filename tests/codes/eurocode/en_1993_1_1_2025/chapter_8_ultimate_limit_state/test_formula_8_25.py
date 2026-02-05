"""Testing formula 8.25 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_25 import Form8Dot25ShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot25ShearStress:
    """Validation for formula 8.25 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 1000.0
        s = 2000.0
        i = 3000.0
        t = 4.0

        # Object to test
        formula = Form8Dot25ShearStress(v_ed=v_ed, s=s, i=i, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 166.66666666666666  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "s", "i", "t"),
        [
            (-1000.0, 2000.0, 3000.0, 4.0),  # v_ed is negative
            (1000.0, -2000.0, 3000.0, 4.0),  # s is negative
            (1000.0, 2000.0, 0.0, 4.0),  # i is zero
            (1000.0, 2000.0, 3000.0, 0.0),  # t is zero
            (1000.0, 2000.0, -3000.0, 4.0),  # i is negative
            (1000.0, 2000.0, 3000.0, -4.0),  # t is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, s: float, i: float, t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot25ShearStress(v_ed=v_ed, s=s, i=i, t=t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Ed} = \frac{V_{Ed} \cdot S}{I \cdot t} = \frac{1000.000 \cdot 2000.000}{3000.000 \cdot 4.000} = 166.667 \ MPa",
            ),
            ("short", r"\tau_{Ed} = 166.667 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 1000.0
        s = 2000.0
        i = 3000.0
        t = 4.0

        # Object to test
        latex = Form8Dot25ShearStress(v_ed=v_ed, s=s, i=i, t=t).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
