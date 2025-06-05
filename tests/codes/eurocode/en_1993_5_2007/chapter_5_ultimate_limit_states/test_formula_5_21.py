"""Testing formula 5.21 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_21 import Form5Dot21ReducedMomentResistanceClass2UProfiles
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot21ReducedMomentResistanceClass2UProfiles:
    """Validation for formula 5.21 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_c_rd = 50.0  # kNm
        n_ed = 20.0  # kN
        n_pl_rd = 40.0  # kN

        # Object to test
        formula = Form5Dot21ReducedMomentResistanceClass2UProfiles(m_c_rd=m_c_rd, n_ed=n_ed, n_pl_rd=n_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 33.25  # kNm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_c_rd", "n_ed", "n_pl_rd"),
        [
            (-50.0, 20.0, 40.0),  # m_c_rd is negative
            (50.0, -20.0, 40.0),  # n_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_c_rd: float, n_ed: float, n_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form5Dot21ReducedMomentResistanceClass2UProfiles(m_c_rd=m_c_rd, n_ed=n_ed, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("m_c_rd", "n_ed", "n_pl_rd"),
        [
            (50.0, 20.0, 0.0),  # n_pl_rd is zero
            (50.0, 20.0, -40.0),  # n_pl_rd is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, m_c_rd: float, n_ed: float, n_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot21ReducedMomentResistanceClass2UProfiles(m_c_rd=m_c_rd, n_ed=n_ed, n_pl_rd=n_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{N,Rd} = 1.33 \cdot M_{c,Rd} \cdot \left(1 - \frac{N_{Ed}}{N_{pl,Rd}}\right) = "
                r"1.33 \cdot 50.000 \cdot \left(1 - \frac{20.000}{40.000}\right) = 33.250 \ kNm",
            ),
            ("short", r"M_{N,Rd} = 33.250 \ kNm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_c_rd = 50.0  # kNm
        n_ed = 20.0  # kN
        n_pl_rd = 40.0  # kN

        # Object to test
        latex = Form5Dot21ReducedMomentResistanceClass2UProfiles(m_c_rd=m_c_rd, n_ed=n_ed, n_pl_rd=n_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
