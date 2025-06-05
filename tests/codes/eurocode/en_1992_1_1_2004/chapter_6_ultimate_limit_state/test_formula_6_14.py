"""Testing formula 6.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_14 import (
    Form6Dot14MaxShearResistanceInclinedReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot14MaxShearResistanceInclinedReinforcement:
    """Validation for formula 6.14 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        alpha_cw = 1.0  # dimensionless
        b_w = 300.0  # mm
        z = 400.0  # mm
        nu_1 = 0.6  # dimensionless
        f_cd = 30.0  # MPa
        theta = 30.0  # degrees
        alpha = 45.0  # degrees

        # Object to test
        formula = Form6Dot14MaxShearResistanceInclinedReinforcement(alpha_cw=alpha_cw, b_w=b_w, z=z, nu_1=nu_1, f_cd=f_cd, theta=theta, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 1475307.43609  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha_cw", "b_w", "z", "nu_1", "f_cd", "theta", "alpha"),
        [
            (-1.0, 300.0, 400.0, 0.6, 30.0, 30.0, 45.0),  # alpha_cw is negative
            (1.0, -300.0, 400.0, 0.6, 30.0, 30.0, 45.0),  # b_w is negative
            (1.0, 300.0, -400.0, 0.6, 30.0, 30.0, 45.0),  # z is negative
            (1.0, 300.0, 400.0, -0.6, 30.0, 30.0, 45.0),  # nu_1 is negative
            (1.0, 300.0, 400.0, 0.6, -30.0, 30.0, 45.0),  # f_cd is negative
            (1.0, 300.0, 400.0, 0.6, 30.0, -30.0, 45.0),  # theta is negative
            (1.0, 300.0, 400.0, 0.6, 30.0, 30.0, -45.0),  # alpha is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, alpha_cw: float, b_w: float, z: float, nu_1: float, f_cd: float, theta: float, alpha: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot14MaxShearResistanceInclinedReinforcement(alpha_cw=alpha_cw, b_w=b_w, z=z, nu_1=nu_1, f_cd=f_cd, theta=theta, alpha=alpha)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Rd,max} = \alpha_{cw} \cdot b_{w} \cdot z \cdot \nu_{1} \cdot f_{cd} \cdot \frac{\cot(\theta) + "
                r"\cot(\alpha)}{1 + \cot^2(\theta)} = 1.000 \cdot 300.000 \cdot 400.000 \cdot 0.600 \cdot 30.000 \cdot "
                r"\frac{\cot(30.000) + \cot(45.000)}{1 + \cot^2(30.000)} = 1475307.436 \ N",
            ),
            ("short", r"V_{Rd,max} = 1475307.436 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha_cw = 1.0  # dimensionless
        b_w = 300.0  # mm
        z = 400.0  # mm
        nu_1 = 0.6  # dimensionless
        f_cd = 30.0  # MPa
        theta = 30.0  # degrees
        alpha = 45.0  # degrees

        # Object to test
        latex = Form6Dot14MaxShearResistanceInclinedReinforcement(
            alpha_cw=alpha_cw, b_w=b_w, z=z, nu_1=nu_1, f_cd=f_cd, theta=theta, alpha=alpha
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
