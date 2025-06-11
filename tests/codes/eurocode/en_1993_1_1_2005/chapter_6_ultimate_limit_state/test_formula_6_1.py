"""Testing formula 6.1 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_1 import Form6Dot1ElasticVerification
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot1ElasticVerification:
    """Validation for formula 6.1 from EN 1993-1-1+C2+A1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_x_ed = 100.0  # MPa
        sigma_z_ed = 50.0  # MPa
        tau_ed = 30.0  # MPa
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless

        # Object to test
        formula = Form6Dot1ElasticVerification(
            sigma_x_ed=sigma_x_ed,
            sigma_z_ed=sigma_z_ed,
            tau_ed=tau_ed,
            f_y=f_y,
            gamma_m0=gamma_m0,
        )

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("sigma_x_ed", "sigma_z_ed", "tau_ed", "f_y", "gamma_m0"),
        [
            (-100.0, 50.0, 30.0, 355.0, 1.0),  # sigma_x_ed is negative
            (100.0, -50.0, 30.0, 355.0, 1.0),  # sigma_z_ed is negative
            (100.0, 50.0, -30.0, 355.0, 1.0),  # tau_ed is negative
            (100.0, 50.0, 30.0, -355.0, 1.0),  # f_y is negative
            (100.0, 50.0, 30.0, 355.0, -1.0),  # gamma_m0 is negative
            (100.0, 50.0, 30.0, 355.0, 0.0),  # gamma_m0 is zero
            (100.0, 50.0, 30.0, 0.0, 1.0),  # f_y is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, sigma_x_ed: float, sigma_z_ed: float, tau_ed: float, f_y: float, gamma_m0: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot1ElasticVerification(
                sigma_x_ed=sigma_x_ed,
                sigma_z_ed=sigma_z_ed,
                tau_ed=tau_ed,
                f_y=f_y,
                gamma_m0=gamma_m0,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{\sigma_{x,\text{Ed}}}{f_y / \gamma_{M0}} \right)^2 + "
                r"\left( \frac{\sigma_{z,\text{Ed}}}{f_y / \gamma_{M0}} \right)^2 - "
                r"\left( \frac{\sigma_{x,\text{Ed}}}{f_y / \gamma_{M0}} \right) "
                r"\left( \frac{\sigma_{z,\text{Ed}}}{f_y / \gamma_{M0}} \right) "
                r"+ 3 \left( \frac{\tau_{\text{Ed}}}{f_y / \gamma_{M0}} \right)^2 \leq 1 \to "
                r"\left( \frac{100.000}{355.000 / 1.000} \right)^2 + "
                r"\left( \frac{50.000}{355.000 / 1.000} \right)^2 - "
                r"\left( \frac{100.000}{355.000 / 1.000} \right) \left( \frac{50.000}{355.000 / 1.000} \right) "
                r"+ 3 \left( \frac{30.000}{355.000 / 1.000} \right)^2 \leq 1 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_x_ed = 100.0  # MPa
        sigma_z_ed = 50.0  # MPa
        tau_ed = 30.0  # MPa
        f_y = 355.0  # MPa
        gamma_m0 = 1.0  # dimensionless

        # Object to test
        latex = Form6Dot1ElasticVerification(
            sigma_x_ed=sigma_x_ed,
            sigma_z_ed=sigma_z_ed,
            tau_ed=tau_ed,
            f_y=f_y,
            gamma_m0=gamma_m0,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
