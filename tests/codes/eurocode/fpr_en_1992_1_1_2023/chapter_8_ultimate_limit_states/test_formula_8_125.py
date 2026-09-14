"""Testing formula 8.125 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_125 import (
    Form8Dot125TransverseTieForceNearEdge,
)
from blueprints.validations import NegativeValueError

# Angle chosen so that its tangent is a round number, which keeps the hand calculation readable
THETA_TAN_0_25 = 14.036243467926479  # tan(theta_cf) = 0.25


class TestForm8Dot125TransverseTieForceNearEdge:
    """Validation for formula 8.125 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_d = 100000.0
        theta_cf = THETA_TAN_0_25

        # Object to test
        formula = Form8Dot125TransverseTieForceNearEdge(f_d=f_d, theta_cf=theta_cf)

        # Expected result, manually calculated: 100000 * 0.25
        manually_calculated_result = 25000.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_d", "theta_cf"),
        [
            (-100000.0, THETA_TAN_0_25),  # f_d is negative
            (100000.0, -14.0),  # theta_cf is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_d: float, theta_cf: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot125TransverseTieForceNearEdge(f_d=f_d, theta_cf=theta_cf)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"F_{td} = F_d \cdot \tan(\theta_{cf}) = 100000.000 \cdot \tan(14.036) = 25000.000 \ N",
            ),
            (
                "complete_with_units",
                r"F_{td} = F_d \cdot \tan(\theta_{cf}) = 100000.000 \ N \cdot \tan(14.036 ^\circ) = 25000.000 \ N",
            ),
            ("short", r"F_{td} = 25000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_d = 100000.0
        theta_cf = THETA_TAN_0_25

        # Object to test
        latex = Form8Dot125TransverseTieForceNearEdge(f_d=f_d, theta_cf=theta_cf).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
