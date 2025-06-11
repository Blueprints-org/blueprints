"""Testing formula 6.23 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_23 import Form6Dot23CheckTorsionalMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot23CheckTorsionalMoment:
    """Validation for formula 6.23 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t_ed = 500.0
        t_rd = 1000.0

        # Object to test
        formula = Form6Dot23CheckTorsionalMoment(t_ed=t_ed, t_rd=t_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("t_ed", "t_rd"),
        [
            (-500.0, 1000.0),  # t_ed is negative
            (500.0, 0.0),  # t_rd is zero
            (500.0, -1000.0),  # t_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t_ed: float, t_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot23CheckTorsionalMoment(t_ed=t_ed, t_rd=t_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{T_{Ed}}{T_{Rd}} \leq 1.0 \right) \to "
                r"\left( \frac{500.000}{1000.000} \leq 1.0 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t_ed = 500.0
        t_rd = 1000.0

        # Object to test
        latex = Form6Dot23CheckTorsionalMoment(t_ed=t_ed, t_rd=t_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
