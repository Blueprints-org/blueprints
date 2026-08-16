"""Testing formula 8.82 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_82 import (
    Form8Dot82TorsionalStressResistanceShearReinforcement,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angle chosen so that its cotangent is a round number, which keeps the hand calculation readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2


class TestForm8Dot82TorsionalStressResistanceShearReinforcement:
    """Validation for formula 8.82 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw = 100.0
        t_eff = 120.0
        s = 200.0
        f_ywd = 435.0

        # Object to test
        formula = Form8Dot82TorsionalStressResistanceShearReinforcement(theta=THETA_COT_2, a_sw=a_sw, t_eff=t_eff, s=s, f_ywd=f_ywd)

        # Expected result, manually calculated: 2 * 100 / (120 * 200) * 435 = 2 * 100 / 24000 * 435
        manually_calculated_result = 3.625  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta", "a_sw", "t_eff", "s", "f_ywd"),
        [
            (THETA_COT_2, -100.0, 120.0, 200.0, 435.0),  # a_sw is negative
            (THETA_COT_2, 100.0, 120.0, 200.0, -435.0),  # f_ywd is negative
            (-THETA_COT_2, 100.0, 120.0, 200.0, 435.0),  # theta is negative
            (0.0, 100.0, 120.0, 200.0, 435.0),  # theta is zero, for which the cotangent diverges
            (THETA_COT_2, 100.0, -120.0, 200.0, 435.0),  # t_eff is negative
            (THETA_COT_2, 100.0, 0.0, 200.0, 435.0),  # t_eff is zero
            (THETA_COT_2, 100.0, 120.0, -200.0, 435.0),  # s is negative
            (THETA_COT_2, 100.0, 120.0, 0.0, 435.0),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, theta: float, a_sw: float, t_eff: float, s: float, f_ywd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot82TorsionalStressResistanceShearReinforcement(theta=theta, a_sw=a_sw, t_eff=t_eff, s=s, f_ywd=f_ywd)

    def test_raise_error_when_theta_exceeds_90_degrees(self) -> None:
        """Test an angle beyond the range of the cotangent."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot82TorsionalStressResistanceShearReinforcement(theta=120.0, a_sw=100.0, t_eff=120.0, s=200.0, f_ywd=435.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{t,Rd,sw} = \cot(\theta) \cdot \frac{A_{sw}}{t_{eff} \cdot s} \cdot f_{ywd} = "
                    r"\cot(26.565) \cdot \frac{100.000}{120.000 \cdot 200.000} \cdot 435.000 = 3.625 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{t,Rd,sw} = \cot(\theta) \cdot \frac{A_{sw}}{t_{eff} \cdot s} \cdot f_{ywd} = "
                    r"\cot(26.565 ^\circ) \cdot \frac{100.000 \ mm^2}{120.000 \ mm \cdot 200.000 \ mm} \cdot 435.000 \ MPa = 3.625 \ MPa"
                ),
            ),
            ("short", r"\tau_{t,Rd,sw} = 3.625 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot82TorsionalStressResistanceShearReinforcement(
            theta=THETA_COT_2,
            a_sw=100.0,
            t_eff=120.0,
            s=200.0,
            f_ywd=435.0,
        ).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
