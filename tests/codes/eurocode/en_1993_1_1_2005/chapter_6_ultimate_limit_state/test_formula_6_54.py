"""Testing formula 6.54 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_54 import (
    Form6Dot54BucklingResistanceOfMembersInBending,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot54BucklingResistanceOfMembersInBending:
    """Validation for formula 6.54 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_ed = 50000.0  # Nmm
        m_b_rd = 100000.0  # Nmm

        # Object to test
        formula = Form6Dot54BucklingResistanceOfMembersInBending(
            m_ed=m_ed, m_b_rd=m_b_rd
        )

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result
        assert formula.unity_check == m_ed / m_b_rd

    @pytest.mark.parametrize(
        ("m_ed", "m_b_rd"),
        [
            (50000.0, 0.0),  # m_b_rd is zero
            (50000.0, -100000.0),  # m_b_rd is negative
            (-50000.0, 100000.0),  # m_ed is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, m_ed: float, m_b_rd: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form6Dot54BucklingResistanceOfMembersInBending(
                m_ed=m_ed, m_b_rd=m_b_rd
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{M_{Ed}}{M_{b,Rd}} \leq 1.0 \to "
                r"\frac{50000.000}{100000.000} \leq 1.0 \to "
                r"\left( 0.500 \leq 1.0 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
            (
                "complete_with_units",
                r"CHECK \to \frac{M_{Ed}}{M_{b,Rd}} \leq 1.0 \to "
                r"\frac{50000.000 \ Nmm}{100000.000 \ Nmm} \leq 1.0 \to "
                r"\left( 0.500 \leq 1.0 \right) \to OK",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_ed = 50000.0  # Nmm
        m_b_rd = 100000.0  # Nmm

        # Object to test
        latex = Form6Dot54BucklingResistanceOfMembersInBending(
            m_ed=m_ed, m_b_rd=m_b_rd
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
            "complete_with_units": latex.complete_with_units,
        }

        assert expected == actual[representation], (
            f"{representation} representation failed."
        )
