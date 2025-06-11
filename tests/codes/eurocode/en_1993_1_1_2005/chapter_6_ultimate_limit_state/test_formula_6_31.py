"""Testing formula 6.31 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_31 import Form6Dot31CheckBendingAndAxialForce
from blueprints.validations import NegativeValueError


class TestForm6Dot31CheckBendingAndAxialForce:
    """Validation for formula 6.31 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_ed = 500.0
        m_n_rd = 600.0

        # Object to test
        formula = Form6Dot31CheckBendingAndAxialForce(m_ed=m_ed, m_n_rd=m_n_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_ed = 700.0
        m_n_rd = 600.0

        # Object to test
        formula = Form6Dot31CheckBendingAndAxialForce(m_ed=m_ed, m_n_rd=m_n_rd)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("m_ed", "m_n_rd"),
        [
            (-500.0, 600.0),  # m_ed is negative
            (500.0, -600.0),  # m_n_rd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_ed: float, m_n_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot31CheckBendingAndAxialForce(m_ed=m_ed, m_n_rd=m_n_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to M_{Ed} \leq M_{N,Rd} \to 500.000 \leq 600.000 \to OK",
            ),
            (
                "complete_with_units",
                r"CHECK \to M_{Ed} \leq M_{N,Rd} \to 500.000 \ Nmm \leq 600.000 \ Nmm \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_ed = 500.0
        m_n_rd = 600.0

        # Object to test
        latex = Form6Dot31CheckBendingAndAxialForce(m_ed=m_ed, m_n_rd=m_n_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
