"""Testing formula 8.123 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_123 import (
    Form8Dot123TransverseTieForceSpreadingForces,
)
from blueprints.validations import NegativeValueError

# Angle chosen so that its tangent is a round number, which keeps the hand calculation readable
THETA_TAN_0_5 = 26.56505117707799  # tan(theta_cf) = 0.5


class TestForm8Dot123TransverseTieForceSpreadingForces:
    """Validation for formula 8.123 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_d = 100000.0
        theta_cf = THETA_TAN_0_5

        # Object to test
        formula = Form8Dot123TransverseTieForceSpreadingForces(f_d=f_d, theta_cf=theta_cf)

        # Expected result, manually calculated: (100000 / 2) * 0.5
        manually_calculated_result = 25000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_d", "theta_cf"),
        [
            (-100000.0, THETA_TAN_0_5),  # f_d is negative
            (100000.0, -30.0),  # theta_cf is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_d: float, theta_cf: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot123TransverseTieForceSpreadingForces(f_d=f_d, theta_cf=theta_cf)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"F_{td} = \frac{F_d}{2} \cdot \tan(\theta_{cf}) = "
                    r"\frac{100000.000}{2} \cdot \tan(26.565) = 25000.000 \ N"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"F_{td} = \frac{F_d}{2} \cdot \tan(\theta_{cf}) = "
                    r"\frac{100000.000 \ N}{2} \cdot \tan(26.565 ^\circ) = 25000.000 \ N"
                ),
            ),
            ("short", r"F_{td} = 25000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_d = 100000.0
        theta_cf = THETA_TAN_0_5

        # Object to test
        latex = Form8Dot123TransverseTieForceSpreadingForces(f_d=f_d, theta_cf=theta_cf).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
