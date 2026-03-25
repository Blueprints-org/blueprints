"""Testing formula 8.19 from EN 1993-1-1:2022, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2022.chapter_8_ultimate_limit_state.formula_8_19 import Form8Dot19CheckBendingMoment
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot19CheckBendingMoment:
    """Validation for formula 8.19 from EN 1993-1-1:2022, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_ed = 1000.0
        m_c_rd = 1500.0

        # Object to test
        formula = Form8Dot19CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

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
            Form8Dot19CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{M_{Ed}}{M_{c,Rd}} \leq 1.0 \to \frac{1000.000}{1500.000} \leq 1.0 \to \left( 0.667 \leq 1.0 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
            (
                "complete_with_units",
                r"CHECK \to \frac{M_{Ed}}{M_{c,Rd}} \leq 1.0 \to \frac{1000.000 \ Nmm}{1500.000 \ Nmm} \leq 1.0 "
                r"\to \left( 0.667 \leq 1.0 \right) \to OK",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_ed = 1000.0
        m_c_rd = 1500.0

        # Object to test
        latex = Form8Dot19CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
            "complete_with_units": latex.complete_with_units,
        }

        assert expected == actual[representation], f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{M_{Ed}}{M_{c,Rd}} \leq 1.0 \to \frac{2000.000}{1500.000} \leq 1.0 \to "
                r"\left( 1.333 \leq 1.0 \right) \to \text{Not OK}",
            ),
        ],
    )
    def test_latex_exceeds_unity(self, representation: str, expected: str) -> None:
        """Test the latex representation when the unity check fails."""
        # Example values — UC = 2000/1500 = 1.333 > 1.0
        m_ed = 2000.0
        m_c_rd = 1500.0

        latex = Form8Dot19CheckBendingMoment(m_ed=m_ed, m_c_rd=m_c_rd).latex()

        actual = {
            "complete": latex.complete,
        }

        assert expected == actual[representation], f"{representation} representation failed."
