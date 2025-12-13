"""Testing formula 6.9 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_9 import Form6Dot9CheckCompressionForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot9CheckCompressionForce:
    """Validation for formula 6.9 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 100.0
        n_c_rd = 150.0

        # Object to test
        formula = Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("n_ed", "n_c_rd"),
        [
            (100.0, 0.0),  # n_c_rd is zero
            (-100.0, 150.0),  # n_ed is negative
            (100.0, -150.0),  # n_c_rd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, n_c_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right) \to "
                r"\left( \frac{100.000}{150.000} \leq 1 \right) \to \left( 0.667 \leq 1 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 100.0
        n_c_rd = 150.0

        # Object to test
        latex = Form6Dot9CheckCompressionForce(n_ed=n_ed, n_c_rd=n_c_rd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
