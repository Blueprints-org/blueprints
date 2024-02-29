"""Testing formula 6.5 of NEN-EN 1993-1-1+C2+A1:2016."""
import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_6_ultimate_limit_state.formula_6_5 import (
    Form6Dot5UnityCheckTensileStrength,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot5UnityCheckTensileStrength:
    """Validation for formula 6.5 from NEN-EN 1993-1-1+C2+A1:2016."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n_ed = 7  # kN
        n_t_rd = 10  # kN
        form = Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)

        # Expected result, manually calculated
        expected = 0.7

        assert form == pytest.approx(expected)

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
            (7, 0),  # n_ed is negative
            (7, -10),  # n_t_rd is negative
        ],
    )
    def test_raise_error_when_negative_or_zero_n_t_rd_is_given(self, n_ed: float, n_t_rd: float) -> None:
        """Test a zero value for n_t_rd."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot5UnityCheckTensileStrength(n_ed=n_ed, n_t_rd=n_t_rd)
