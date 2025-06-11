"""Testing formula 6.40 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_40 import Form6Dot40ReducedBendingMomentResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot40ReducedBendingMomentResistance:
    """Validation for formula 6.40 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        mpl_z_rd = 6000.0
        n = 0.3
        a_f = 0.4

        formula = Form6Dot40ReducedBendingMomentResistance(mpl_z_rd=mpl_z_rd, n=n, a_f=a_f)
        manually_calculated_result = 5250.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("mpl_z_rd", "n", "a_f"),
        [
            (-6000.0, 0.3, 0.4),  # mpl_z_rd is negative
            (6000.0, -0.3, 0.4),  # n is negative
            (6000.0, 0.3, -0.4),  # a_f is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, mpl_z_rd: float, n: float, a_f: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot40ReducedBendingMomentResistance(mpl_z_rd=mpl_z_rd, n=n, a_f=a_f)

    @pytest.mark.parametrize(
        ("mpl_z_rd", "n", "a_f"),
        [
            (6000.0, 0.3, 2.0),  # denominator (1 - 0.5 * a_f) <= 0
        ],
    )
    def test_raise_error_when_denominator_is_invalid(self, mpl_z_rd: float, n: float, a_f: float) -> None:
        """Test invalid denominator."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot40ReducedBendingMomentResistance(mpl_z_rd=mpl_z_rd, n=n, a_f=a_f)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,z,Rd} = \min \left( M_{pl,z,Rd} \cdot \frac{1 - n}{1 - 0.5 \cdot a_f}, M_{pl,z,Rd} \right) = "
                r"\min \left( 6000.000 \cdot \frac{1 - 0.300}{1 - 0.5 \cdot 0.400}, 6000.000 \right) = 5250.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,z,Rd} = \min \left( M_{pl,z,Rd} \cdot \frac{1 - n}{1 - 0.5 \cdot a_f}, M_{pl,z,Rd} \right) = "
                r"\min \left( 6000.000 \ Nmm \cdot \frac{1 - 0.300}{1 - 0.5 \cdot 0.400}, 6000.000 \ Nmm \right) = 5250.000 \ Nmm",
            ),
            ("short", r"M_{N,z,Rd} = 5250.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        mpl_z_rd = 6000.0
        n = 0.3
        a_f = 0.4

        latex = Form6Dot40ReducedBendingMomentResistance(mpl_z_rd=mpl_z_rd, n=n, a_f=a_f).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
