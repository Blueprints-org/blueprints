"""Testing formula 6.46 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_46 import (
    Form6Dot46BucklingResistanceOfMembersInCompression,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot46BucklingResistanceOfMembersInCompression:
    """Validation for formula 6.46 from EN 1993-1-1:2005."""

    @pytest.mark.parametrize(
        ("n_ed", "n_b_rd", "expected", "expected_unity_check"),
        [
            (500000.0, 800000.0, True, 0.625),  # check passes: 500000 / 800000 = 0.625
            (800000.0, 800000.0, True, 1.0),  # exactly on the limit
            (900000.0, 800000.0, False, 1.125),  # check fails: 900000 / 800000 = 1.125
        ],
    )
    def test_evaluation(self, n_ed: float, n_b_rd: float, expected: bool, expected_unity_check: float) -> None:
        """Tests the evaluation of the result."""
        formula = Form6Dot46BucklingResistanceOfMembersInCompression(n_ed=n_ed, n_b_rd=n_b_rd)

        assert bool(formula) is expected
        assert formula.unity_check == pytest.approx(expected=expected_unity_check, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "n_b_rd"),
        [
            (-500000.0, 800000.0),  # n_ed is negative
            (500000.0, 0.0),  # n_b_rd is zero
            (500000.0, -800000.0),  # n_b_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, n_b_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot46BucklingResistanceOfMembersInCompression(n_ed=n_ed, n_b_rd=n_b_rd)

    @pytest.mark.parametrize(
        ("n_ed", "representation", "expected"),
        [
            (
                500000.0,
                "complete",
                (
                    r"CHECK \to \frac{N_{Ed}}{N_{b,Rd}} \leq 1.0 \to \frac{500000.000}{800000.000} \leq 1.0 \to "
                    r"\left( 0.625 \leq 1.0 \right) \to OK"
                ),
            ),
            (
                500000.0,
                "complete_with_units",
                (
                    r"CHECK \to \frac{N_{Ed}}{N_{b,Rd}} \leq 1.0 \to \frac{500000.000 \ N}{800000.000 \ N} \leq 1.0 \to "
                    r"\left( 0.625 \leq 1.0 \right) \to OK"
                ),
            ),
            (500000.0, "short", r"CHECK \to OK"),
            (900000.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, n_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_b_rd = 800000.0

        # Object to test
        latex = Form6Dot46BucklingResistanceOfMembersInCompression(n_ed=n_ed, n_b_rd=n_b_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
