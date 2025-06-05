"""Testing formula 6.9 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_9 import Form6Dot9MaximumShearResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot9MaximumShearResistance:
    """Validation for formula 6.9 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        b_w = 300.0
        z = 500.0
        f_cd = 25.0
        nu_1 = 0.6
        alpha_cw = 1.0
        theta = 30.0

        # Object to test
        formula = Form6Dot9MaximumShearResistance(b_w=b_w, z=z, f_cd=f_cd, nu_1=nu_1, alpha_cw=alpha_cw, theta=theta)

        # Expected result, manually calculated
        manually_calculated_result = 974278.579257  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_w", "z", "f_cd", "nu_1", "alpha_cw", "theta"),
        [
            (-300.0, 500.0, 25.0, 0.6, 1.0, 30.0),  # b_w is negative
            (300.0, -500.0, 25.0, 0.6, 1.0, 30.0),  # z is negative
            (300.0, 500.0, -25.0, 0.6, 1.0, 30.0),  # f_cd is negative
            (300.0, 500.0, 25.0, -0.6, 1.0, 30.0),  # nu_1 is negative
            (300.0, 500.0, 25.0, 0.6, -1.0, 30.0),  # alpha_cw is negative
            (300.0, 500.0, 25.0, 0.6, 1.0, -30.0),  # theta is negative
            (300.0, 500.0, 25.0, 0.6, 1.0, 0.0),  # theta is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_w: float, z: float, f_cd: float, nu_1: float, alpha_cw: float, theta: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot9MaximumShearResistance(b_w=b_w, z=z, f_cd=f_cd, nu_1=nu_1, alpha_cw=alpha_cw, theta=theta)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Rd,max} = \alpha_{cw} \cdot b_{w} \cdot z \cdot \nu_{1} \cdot \frac{f_{cd}}{\cot(\theta) + \tan(\theta)} = "
                r"1.000 \cdot 300.000 \cdot 500.000 \cdot 0.600 \cdot \frac{25.000}{\cot(30.000) + \tan(30.000)} = 974278.579 \ N",
            ),
            ("short", r"V_{Rd,max} = 974278.579 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_w = 300.0
        z = 500.0
        f_cd = 25.0
        nu_1 = 0.6
        alpha_cw = 1.0
        theta = 30.0

        # Object to test
        latex = Form6Dot9MaximumShearResistance(b_w=b_w, z=z, f_cd=f_cd, nu_1=nu_1, alpha_cw=alpha_cw, theta=theta).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
