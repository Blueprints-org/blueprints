"""Testing formula 6.33 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_33 import Form6Dot33CheckAxialForceY
from blueprints.validations import NegativeValueError


class TestForm6Dot33CheckAxialForceY:
    """Validation for formula 6.33 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        n_ed = 50.0
        n_pl_rd = 300.0

        formula = Form6Dot33CheckAxialForceY(n_ed=n_ed, n_pl_rd=n_pl_rd)

        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        "n_pl_rd",
        [-300.0],  # n_pl_rd is negative
    )
    def test_raise_error_when_invalid_values_are_given(self, n_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot33CheckAxialForceY(n_ed=50.0, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to N_{Ed} \leq 0.25 \cdot N_{pl,Rd} \to 50.000 \leq 0.25 \cdot 300.000 \to OK",
            ),
            (
                "complete_with_units",
                r"CHECK \to N_{Ed} \leq 0.25 \cdot N_{pl,Rd} \to 50.000 \ N \leq 0.25 \cdot 300.000 \ N \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        n_ed = 50.0
        n_pl_rd = 300.0

        latex = Form6Dot33CheckAxialForceY(n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
