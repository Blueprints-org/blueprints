"""Testing formula 8.30 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_30 import (
    Form8Dot30CheckCombinedShearForceAndTorsionalMoment,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot30CheckCombinedShearForceAndTorsionalMoment:
    """Validation for formula 8.30 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100.0
        v_pl_t_rd = 150.0

        # Object to test
        formula = Form8Dot30CheckCombinedShearForceAndTorsionalMoment(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_t_rd"),
        [
            (-100.0, 150.0),  # v_ed is negative
            (100.0, -150.0),  # v_pl_t_rd is negative
            (100.0, 0.0),  # v_pl_t_rd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, v_pl_t_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot30CheckCombinedShearForceAndTorsionalMoment(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{V_{Ed}}{V_{pl,T,Rd}} \leq 1.0 \right) \to "
                r"\left( \frac{100.000}{150.000} \leq 1.0 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 100.0
        v_pl_t_rd = 150.0

        # Object to test
        latex = Form8Dot30CheckCombinedShearForceAndTorsionalMoment(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
