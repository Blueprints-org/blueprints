"""Testing formula 8.119 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_119 import (
    Form8Dot119StrengthReductionFactorCrossedByTieRefined,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError

# Angle chosen so that its cotangent is a round number, which keeps the hand calculation readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2


class TestForm8Dot119StrengthReductionFactorCrossedByTieRefined:
    """Validation for formula 8.119 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example value
        theta_cs = THETA_COT_2

        # Object to test
        formula = Form8Dot119StrengthReductionFactorCrossedByTieRefined(theta_cs=theta_cs)

        # Expected result, manually calculated: 1 / (1.11 + 0.22 * 2**2) = 1 / 1.99
        manually_calculated_result = 0.5025125628140705

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "theta_cs",
        [
            0.0,  # zero
            -5.0,  # negative
        ],
    )
    def test_raise_error_when_theta_cs_is_less_or_equal_to_zero(self, theta_cs: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot119StrengthReductionFactorCrossedByTieRefined(theta_cs=theta_cs)

    def test_raise_error_when_theta_cs_is_greater_than_90(self) -> None:
        """Test invalid value beyond the valid range of the cotangent."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot119StrengthReductionFactorCrossedByTieRefined(theta_cs=95.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\nu = \frac{1}{1.11 + 0.22 \cdot \left(\cot(\theta_{cs})\right)^2} = "
                    r"\frac{1}{1.11 + 0.22 \cdot \left(\cot(26.565)\right)^2} = 0.503 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\nu = \frac{1}{1.11 + 0.22 \cdot \left(\cot(\theta_{cs})\right)^2} = "
                    r"\frac{1}{1.11 + 0.22 \cdot \left(\cot(26.565 ^\circ)\right)^2} = 0.503 \ -"
                ),
            ),
            ("short", r"\nu = 0.503 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example value
        theta_cs = THETA_COT_2

        # Object to test
        latex = Form8Dot119StrengthReductionFactorCrossedByTieRefined(theta_cs=theta_cs).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
