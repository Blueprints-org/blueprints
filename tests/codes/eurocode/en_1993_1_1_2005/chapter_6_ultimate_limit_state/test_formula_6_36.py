"""Testing formula 6.36 from EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_36 import Form6Dot36MomentReduction
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot36MomentReduction:
    """Validation for formula 6.36 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_y_rd = 50000.0
        a = 0.4
        n = 0.5

        # Object to test
        formula = Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, a=a, n=n)

        # Expected result, manually calculated
        manually_calculated_result = 31250.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        mpl_y_rd = 50000.0
        a = 0.4
        n = 0.0

        # Object to test
        formula = Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, a=a, n=n)

        # Expected result, manually calculated
        manually_calculated_result = 50000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("mpl_y_rd", "n"),
        [
            (-50000.0, 0.5),  # mpl_y_rd is negative
            (50000.0, -0.5),  # n is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, mpl_y_rd: float, n: float) -> None:
        """Test invalid negative values."""
        with pytest.raises(NegativeValueError):
            Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, a=0.4, n=n)

    @pytest.mark.parametrize(
        "a",
        [
            2.0,  # denominator will be zero
            -1.0,  # a is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float) -> None:
        """Test invalid zero or negative values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form6Dot36MomentReduction(mpl_y_rd=10000.0, a=a, n=0.5)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,y,Rd} = \min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot (1 - n) / (1 - 0.5 \cdot a)\right) = "
                r"\min\left(50000.000, 50000.000 \cdot (1 - 0.500) / (1 - 0.5 \cdot 0.400)\right) = 31250.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,y,Rd} = \min\left(M_{pl,y,Rd}, M_{pl,y,Rd} \cdot (1 - n) / (1 - 0.5 \cdot a)\right) = "
                r"\min\left(50000.000 \ Nmm, 50000.000 \ Nmm \cdot (1 - 0.500) / (1 - 0.5 \cdot 0.400)\right) = "
                r"31250.000 \ Nmm",
            ),
            ("short", r"M_{N,y,Rd} = 31250.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        mpl_y_rd = 50000.0
        a = 0.4
        n = 0.5

        # Object to test
        latex = Form6Dot36MomentReduction(mpl_y_rd=mpl_y_rd, a=a, n=n).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
