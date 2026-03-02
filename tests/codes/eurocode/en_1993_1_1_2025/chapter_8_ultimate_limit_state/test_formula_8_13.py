"""Testing formula 8.13 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_13 import Form8Dot13UnityCheckTensileStrength
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot13UnityCheckTensileStrength:
    """Validation for formula 8.13 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 7  # kN
        n_t_rd = 10  # kN
        form = Form8Dot13UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

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
            Form8Dot13UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

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
            Form8Dot13UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right) \to "
                r"\left( \frac{7.000}{10.000} \leq 1 \right) \to OK",
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
        latex = Form8Dot13UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
