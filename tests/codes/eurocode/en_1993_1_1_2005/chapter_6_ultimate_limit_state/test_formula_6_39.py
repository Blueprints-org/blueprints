"""Testing formula 6.39 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_39 import Form6Dot39ReducedBendingMomentResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot39ReducedBendingMomentResistance:
    """Validation for formula 6.39 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        mpl_y_rd = 5000.0
        n = 0.2
        a_w = 0.3

        formula = Form6Dot39ReducedBendingMomentResistance(mpl_y_rd=mpl_y_rd, n=n, a_w=a_w)
        manually_calculated_result = 4705.882  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("mpl_y_rd", "n", "a_w"),
        [
            (-5000.0, 0.2, 0.3),  # mpl_y_rd is negative
            (5000.0, -0.2, 0.3),  # n is negative
            (5000.0, 0.2, -0.3),  # a_w is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, mpl_y_rd: float, n: float, a_w: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot39ReducedBendingMomentResistance(mpl_y_rd=mpl_y_rd, n=n, a_w=a_w)

    @pytest.mark.parametrize(
        ("mpl_y_rd", "n", "a_w"),
        [
            (5000.0, 0.2, 2.0),  # denominator (1 - 0.5 * a_w) <= 0
        ],
    )
    def test_raise_error_when_denominator_is_invalid(self, mpl_y_rd: float, n: float, a_w: float) -> None:
        """Test invalid denominator."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot39ReducedBendingMomentResistance(mpl_y_rd=mpl_y_rd, n=n, a_w=a_w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,y,Rd} = \min \left( M_{pl,y,Rd} \cdot \frac{1 - n}{1 - 0.5 \cdot a_w}, M_{pl,y,Rd} \right) = "
                r"\min \left( 5000.000 \cdot \frac{1 - 0.200}{1 - 0.5 \cdot 0.300}, 5000.000 \right) = 4705.882 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,y,Rd} = \min \left( M_{pl,y,Rd} \cdot \frac{1 - n}{1 - 0.5 \cdot a_w}, M_{pl,y,Rd} \right) = "
                r"\min \left( 5000.000 \ Nmm \cdot \frac{1 - 0.200}{1 - 0.5 \cdot 0.300}, 5000.000 \ Nmm \right) = 4705.882 \ Nmm",
            ),
            ("short", r"M_{N,y,Rd} = 4705.882 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        mpl_y_rd = 5000.0
        n = 0.2
        a_w = 0.3

        latex = Form6Dot39ReducedBendingMomentResistance(mpl_y_rd=mpl_y_rd, n=n, a_w=a_w).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
