"""Testing formula 6.13 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_13 import (
    Form6Dot13ShearResistanceInclinedReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot13ShearResistanceInclinedReinforcement:
    """Validation for formula 6.13 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw = 100.0  # mm²
        s = 200.0  # mm
        z = 300.0  # mm
        f_ywd = 400.0  # MPa
        theta = 30.0  # degrees
        alpha = 45.0  # degrees

        # Object to test
        formula = Form6Dot13ShearResistanceInclinedReinforcement(a_sw=a_sw, s=s, z=z, f_ywd=f_ywd, theta=theta, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 115911.099155  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_sw", "s", "z", "f_ywd", "theta", "alpha"),
        [
            (-100.0, 200.0, 300.0, 400.0, 30.0, 45.0),  # a_sw is negative
            (100.0, -200.0, 300.0, 400.0, 30.0, 45.0),  # s is negative
            (100.0, 200.0, -300.0, 400.0, 30.0, 45.0),  # z is negative
            (100.0, 200.0, 300.0, -400.0, 30.0, 45.0),  # f_ywd is negative
            (100.0, 200.0, 300.0, 400.0, -30.0, 45.0),  # theta is negative
            (100.0, 200.0, 300.0, 400.0, 30.0, -45.0),  # alpha is negative
            (100.0, 0.0, 300.0, 400.0, 30.0, 45.0),  # s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sw: float, s: float, z: float, f_ywd: float, theta: float, alpha: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot13ShearResistanceInclinedReinforcement(a_sw=a_sw, s=s, z=z, f_ywd=f_ywd, theta=theta, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Rd,s} = \frac{A_{sw}}{s} \cdot z \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha)\right) \cdot \sin(\alpha) = "
                r"\frac{100.000}{200.000} \cdot 300.000 \cdot 400.000 \cdot \left(\cot(30.000) + \cot(45.000)\right) \cdot \sin(45.000) = "
                r"115911.099 \ N",
            ),
            ("short", r"V_{Rd,s} = 115911.099 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw = 100.0  # mm²
        s = 200.0  # mm
        z = 300.0  # mm
        f_ywd = 400.0  # MPa
        theta = 30.0  # degrees
        alpha = 45.0  # degrees

        # Object to test
        latex = Form6Dot13ShearResistanceInclinedReinforcement(a_sw=a_sw, s=s, z=z, f_ywd=f_ywd, theta=theta, alpha=alpha).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
