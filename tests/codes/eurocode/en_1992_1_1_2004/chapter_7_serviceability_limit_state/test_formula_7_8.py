"""Testing formula 7.8 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_8 import Form7Dot8CrackWidth
from blueprints.validations import NegativeValueError


class TestForm7Dot8CrackWidth:
    """Validation for formula 7.8 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        s_r_max = 200.0
        epsilon_sm_minus_epsilon_cm = 0.001

        # Object to test
        formula = Form7Dot8CrackWidth(s_r_max=s_r_max, epsilon_sm_minus_epsilon_cm=epsilon_sm_minus_epsilon_cm)

        # Expected result, manually calculated
        manually_calculated_result = 0.200  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("s_r_max", "epsilon_sm_minus_epsilon_cm"),
        [
            (-200.0, 0.001),  # s_r_max is negative
            (200.0, -0.001),  # epsilon_sm_minus_epsilon_cm is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, s_r_max: float, epsilon_sm_minus_epsilon_cm: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot8CrackWidth(s_r_max=s_r_max, epsilon_sm_minus_epsilon_cm=epsilon_sm_minus_epsilon_cm)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"w_k = s_{r,max} \cdot (\epsilon_{sm} - \epsilon_{cm}) = 200.000 \cdot (0.001) = 0.200 \ mm",
            ),
            ("short", r"w_k = 0.200 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        s_r_max = 200.0
        epsilon_sm_minus_epsilon_cm = 0.001

        # Object to test
        latex = Form7Dot8CrackWidth(s_r_max=s_r_max, epsilon_sm_minus_epsilon_cm=epsilon_sm_minus_epsilon_cm).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
