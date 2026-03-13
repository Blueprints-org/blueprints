"""Testing formula 6.12 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_12 import Form6Dot12CheckBendingMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot12CheckBendingMoment:
    """Validation for formula 6.12 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_ed = 1000.0
        m_c_rd = 1500.0

        # Object to test
        formula = Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("m_ed", "m_c_rd"),
        [
            (1000.0, 0.0),  # m_c_rd is zero
            (-1000.0, 1500.0),  # m_ed is negative
            (1000.0, -1500.0),  # m_c_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_ed: float, m_c_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{M_{Ed}}{M_{c,Rd}} \leq 1 \right) \to "
                r"\left( \frac{1000.000}{1500.000} \leq 1 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_ed = 1000.0
        m_c_rd = 1500.0

        # Object to test
        latex = Form6Dot12CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
