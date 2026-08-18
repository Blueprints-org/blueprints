"""Testing formula 8.84 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_84 import (
    Form8Dot84TorsionalStressResistanceConcreteCrushing,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angle chosen so that its cotangent and tangent are round numbers, which keeps the hand calculation readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2, tan(theta) = 0.5


class TestForm8Dot84TorsionalStressResistanceConcreteCrushing:
    """Validation for formula 8.84 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        nu = 0.5
        f_cd = 20.0

        # Object to test
        formula = Form8Dot84TorsionalStressResistanceConcreteCrushing(nu=nu, f_cd=f_cd, theta=THETA_COT_2)

        # Expected result, manually calculated: 0.5 * 20 / (2 + 0.5) = 10 / 2.5
        manually_calculated_result = 4.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_at_45_degrees(self) -> None:
        """Tests a second angle, since a single one cannot distinguish the sum of the two functions from a
        multiple of one of them. At 45 degrees the denominator is 1 + 1 and the resistance is at its maximum.
        """
        # Object to test
        formula = Form8Dot84TorsionalStressResistanceConcreteCrushing(nu=0.5, f_cd=20.0, theta=45.0)

        # Expected result, manually calculated: 0.5 * 20 / (1 + 1) = 10 / 2
        manually_calculated_result = 5.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("nu", "f_cd", "theta"),
        [
            (-0.5, 20.0, THETA_COT_2),  # nu is negative
            (0.5, -20.0, THETA_COT_2),  # f_cd is negative
            (0.5, 20.0, -THETA_COT_2),  # theta is negative
            (0.5, 20.0, 0.0),  # theta is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, nu: float, f_cd: float, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot84TorsionalStressResistanceConcreteCrushing(nu=nu, f_cd=f_cd, theta=theta)

    def test_raise_error_when_theta_exceeds_90_degrees(self) -> None:
        """Test an angle beyond the range of the cotangent."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot84TorsionalStressResistanceConcreteCrushing(nu=0.5, f_cd=20.0, theta=120.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{t,Rd,max} = \frac{\nu \cdot f_{cd}}{\cot(\theta) + \tan(\theta)} = "
                    r"\frac{0.500 \cdot 20.000}{\cot(26.565) + \tan(26.565)} = 4.000 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{t,Rd,max} = \frac{\nu \cdot f_{cd}}{\cot(\theta) + \tan(\theta)} = "
                    r"\frac{0.500 \cdot 20.000 \ MPa}{\cot(26.565 ^\circ) + \tan(26.565 ^\circ)} = 4.000 \ MPa"
                ),
            ),
            ("short", r"\tau_{t,Rd,max} = 4.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot84TorsionalStressResistanceConcreteCrushing(nu=0.5, f_cd=20.0, theta=THETA_COT_2).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
