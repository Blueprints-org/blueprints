"""Testing formula 6.5 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_5 import Form6Dot5UnityCheckTensileStrength
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot5UnityCheckTensileStrength:
    """Validation for formula 6.5 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 7  # kN
        n_t_rd = 10  # kN
        form = Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

        # Expected result, manually calculated
        expected = True

        assert form == expected

    @pytest.mark.parametrize(
        ("n_ed", "n_t_rd"),
        [
            (-7, 10),  # n_ed is negative
        ],
    )
    def test_raise_error_when_negative_n_ed_is_given(self, n_ed: float, n_t_rd: float) -> None:
        """Test a negative value for n_ed."""
        with pytest.raises(NegativeValueError):
            Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

    @pytest.mark.parametrize(
        ("n_ed", "n_t_rd"),
        [
            (7, 0),  # n_t_rd is zero
            (7, -10),  # n_t_rd is negative
        ],
    )
    def test_raise_error_when_negative_or_zero_n_t_rd_is_given(self, n_ed: float, n_t_rd: float) -> None:
        """Test a zero or negative value for n_t_rd."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right) \to "
                r"\left( \frac{7.000}{10.000} \leq 1 \right) \to \left( 0.700 \leq 1 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 7  # kN
        n_t_rd = 10  # kN

        # Object to test
        latex = Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
