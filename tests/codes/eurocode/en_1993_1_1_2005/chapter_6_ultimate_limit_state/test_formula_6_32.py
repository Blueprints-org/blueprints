"""Testing formula 6.32 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_32 import Form6Dot32MNrdRectangular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot32MNrdRectangular:
    """Validation for formula 6.32 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_pl_rd = 5000.0  # Nmm
        n_ed = 1000.0  # N
        n_pl_rd = 2000.0  # N

        # Object to test
        formula = Form6Dot32MNrdRectangular(m_pl_rd=m_pl_rd, n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 3750.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_pl_rd", "n_ed", "n_pl_rd"),
        [
            (-5000.0, 1000.0, 2000.0),  # m_pl_rd is negative
            (5000.0, -1000.0, 2000.0),  # n_ed is negative
            (5000.0, 1000.0, -2000.0),  # n_pl_rd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_pl_rd: float, n_ed: float, n_pl_rd: float) -> None:
        """Test invalid negative values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot32MNrdRectangular(m_pl_rd=m_pl_rd, n_ed=n_ed, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("m_pl_rd", "n_ed", "n_pl_rd"),
        [
            (5000.0, 1000.0, 0.0),  # n_pl_rd is zero
        ],
    )
    def test_raise_error_when_zero_values_are_given(self, m_pl_rd: float, n_ed: float, n_pl_rd: float) -> None:
        """Test invalid zero values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot32MNrdRectangular(m_pl_rd=m_pl_rd, n_ed=n_ed, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,Rd} = M_{pl,Rd} \cdot \left[ 1 - \left( \frac{N_{Ed}}{N_{pl,Rd}} \right)^2 \right] = "
                r"5000.000 \cdot \left[ 1 - \left( \frac{1000.000}{2000.000} \right)^2 \right] = 3750.000 \ Nmm",
            ),
            (
                "complete_with_units",
                r"M_{N,Rd} = M_{pl,Rd} \cdot \left[ 1 - \left( \frac{N_{Ed}}{N_{pl,Rd}} \right)^2 \right] = "
                r"5000.000 \ Nmm \cdot \left[ 1 - \left( \frac{1000.000 \ N}{2000.000 \ N} \right)^2 \right] = 3750.000 \ Nmm",
            ),
            ("short", r"M_{N,Rd} = 3750.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_pl_rd = 5000.0  # Nmm
        n_ed = 1000.0  # N
        n_pl_rd = 2000.0  # N

        # Object to test
        latex = Form6Dot32MNrdRectangular(m_pl_rd=m_pl_rd, n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
