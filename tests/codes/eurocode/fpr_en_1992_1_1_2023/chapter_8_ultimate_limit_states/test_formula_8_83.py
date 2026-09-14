"""Testing formula 8.83 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_83 import (
    Form8Dot83TorsionalStressResistanceLongitudinalReinforcement,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angle chosen so that its cotangent is a round number, which keeps the hand calculation readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2


class TestForm8Dot83TorsionalStressResistanceLongitudinalReinforcement:
    """Validation for formula 8.83 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sum_a_sl = 2400.0
        f_yd = 435.0
        t_eff = 120.0
        u_k = 1500.0

        # Object to test
        formula = Form8Dot83TorsionalStressResistanceLongitudinalReinforcement(sum_a_sl=sum_a_sl, f_yd=f_yd, t_eff=t_eff, u_k=u_k, theta=THETA_COT_2)

        # Expected result, manually calculated: 2400 * 435 / (120 * 1500 * 2) = 1044000 / 360000
        manually_calculated_result = 2.9  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sum_a_sl", "f_yd", "t_eff", "u_k", "theta"),
        [
            (-2400.0, 435.0, 120.0, 1500.0, THETA_COT_2),  # sum_a_sl is negative
            (2400.0, -435.0, 120.0, 1500.0, THETA_COT_2),  # f_yd is negative
            (2400.0, 435.0, -120.0, 1500.0, THETA_COT_2),  # t_eff is negative
            (2400.0, 435.0, 0.0, 1500.0, THETA_COT_2),  # t_eff is zero
            (2400.0, 435.0, 120.0, -1500.0, THETA_COT_2),  # u_k is negative
            (2400.0, 435.0, 120.0, 0.0, THETA_COT_2),  # u_k is zero
            (2400.0, 435.0, 120.0, 1500.0, -THETA_COT_2),  # theta is negative
            (2400.0, 435.0, 120.0, 1500.0, 0.0),  # theta is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sum_a_sl: float, f_yd: float, t_eff: float, u_k: float, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot83TorsionalStressResistanceLongitudinalReinforcement(sum_a_sl=sum_a_sl, f_yd=f_yd, t_eff=t_eff, u_k=u_k, theta=theta)

    def test_raise_error_when_theta_exceeds_90_degrees(self) -> None:
        """Test an angle beyond the range of the cotangent."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot83TorsionalStressResistanceLongitudinalReinforcement(sum_a_sl=2400.0, f_yd=435.0, t_eff=120.0, u_k=1500.0, theta=120.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{t,Rd,sl} = \frac{\Sigma A_{sl} \cdot f_{yd}}{t_{eff} \cdot u_k \cdot \cot(\theta)} = "
                    r"\frac{2400.000 \cdot 435.000}{120.000 \cdot 1500.000 \cdot \cot(26.565)} = 2.900 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{t,Rd,sl} = \frac{\Sigma A_{sl} \cdot f_{yd}}{t_{eff} \cdot u_k \cdot \cot(\theta)} = "
                    r"\frac{2400.000 \ mm^2 \cdot 435.000 \ MPa}{120.000 \ mm \cdot 1500.000 \ mm \cdot \cot(26.565 ^\circ)} = 2.900 \ MPa"
                ),
            ),
            ("short", r"\tau_{t,Rd,sl} = 2.900 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot83TorsionalStressResistanceLongitudinalReinforcement(
            sum_a_sl=2400.0,
            f_yd=435.0,
            t_eff=120.0,
            u_k=1500.0,
            theta=THETA_COT_2,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
