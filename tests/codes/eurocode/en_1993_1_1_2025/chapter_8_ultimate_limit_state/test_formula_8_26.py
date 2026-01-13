"""Testing formula 8.26 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_26 import Form8Dot26ShearStressIOrHSection
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot26ShearStressIOrHSection:
    """Validation for formula 8.26 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 1000.0
        a_w = 200.0
        a_f = 150.0

        # Object to test
        formula = Form8Dot26ShearStressIOrHSection(v_ed=v_ed, a_w=a_w, a_f=a_f)

        # Expected result, manually calculated
        manually_calculated_result = 5.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "a_w", "a_f"),
        [
            (-1000.0, 200.0, 150.0),  # v_ed is negative
            (1000.0, 200.0, -150.0),  # a_f is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, a_w: float, a_f: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot26ShearStressIOrHSection(v_ed=v_ed, a_w=a_w, a_f=a_f)

    @pytest.mark.parametrize(
        ("v_ed", "a_w", "a_f"),
        [
            (1000.0, 0.0, 150.0),  # a_w is zero
            (1000.0, -200.0, 150.0),  # a_w is negative
        ],
    )
    def test_raise_error_when_a_w_is_invalid(self, v_ed: float, a_w: float, a_f: float) -> None:
        """Test invalid values for a_w."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot26ShearStressIOrHSection(v_ed=v_ed, a_w=a_w, a_f=a_f)

    @pytest.mark.parametrize(
        ("v_ed", "a_w", "a_f"),
        [
            (1000.0, 200.0, 50.0),  # a_f / a_w < 0.6
        ],
    )
    def test_raise_error_when_a_f_divided_by_a_w_is_invalid(self, v_ed: float, a_w: float, a_f: float) -> None:
        """Test invalid values for a_f / a_w."""
        with pytest.raises(ValueError):
            Form8Dot26ShearStressIOrHSection(v_ed=v_ed, a_w=a_w, a_f=a_f)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Ed} = \frac{V_{Ed}}{A_w} \text{ if } A_f / A_w \ge 0.6 = "
                r"\frac{1000.000}{200.000} \text{ if } 150.000 / 200.000 \ge 0.6 = 5.000 \ MPa",
            ),
            ("short", r"\tau_{Ed} = 5.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 1000.0
        a_w = 200.0
        a_f = 150.0

        # Object to test
        latex = Form8Dot26ShearStressIOrHSection(v_ed=v_ed, a_w=a_w, a_f=a_f).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
