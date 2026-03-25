"""Testing formula 8.22 from EN 1993-1-1:2022, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2022.chapter_8_ultimate_limit_state.formula_8_22 import Form8Dot22CheckShearForce
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot22CheckShearForce:
    """Validation for formula 8.22 from EN 1993-1-1:2022, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100.0
        v_c_rd = 150.0

        # Object to test
        formula = Form8Dot22CheckShearForce(v_ed=v_ed, v_c_rd=v_c_rd)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("v_ed", "v_c_rd"),
        [
            (-100.0, 150.0),  # v_ed is negative
            (100.0, -150.0),  # v_c_rd is negative
            (100.0, 0.0),  # v_c_rd is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, v_c_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot22CheckShearForce(v_ed=v_ed, v_c_rd=v_c_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{V_{Ed}}{V_{c,Rd}} \leq 1.0 \to \frac{100.000}{150.000} \leq 1.0 \to \left( 0.667 \leq 1.0 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
            (
                "complete_with_units",
                r"CHECK \to \frac{V_{Ed}}{V_{c,Rd}} \leq 1.0 \to \frac{100.000 \ N}{150.000 \ N} \leq 1.0 \to \left( 0.667 \leq 1.0 \right) \to OK",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 100.0
        v_c_rd = 150.0

        # Object to test
        latex = Form8Dot22CheckShearForce(v_ed=v_ed, v_c_rd=v_c_rd).latex()

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
                r"CHECK \to \frac{V_{Ed}}{V_{c,Rd}} \leq 1.0 \to \frac{200.000}{150.000} "
                r"\leq 1.0 \to \left( 1.333 \leq 1.0 \right) \to \text{Not OK}",
            ),
        ],
    )
    def test_latex_exceeds_unity(self, representation: str, expected: str) -> None:
        """Test the latex representation when the unity check fails."""
        # Example values — UC = 200/150 = 1.333 > 1.0
        v_ed = 200.0
        v_c_rd = 150.0

        latex = Form8Dot22CheckShearForce(v_ed=v_ed, v_c_rd=v_c_rd).latex()

        actual = {
            "complete": latex.complete,
        }

        assert expected == actual[representation], f"{representation} representation failed."
