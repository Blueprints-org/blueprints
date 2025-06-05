"""Testing formula 7.9 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_9 import Form7Dot9EpsilonSmMinusEpsilonCm
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot9EpsilonSmMinusEpsilonCm:
    """Validation for formula 7.9 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_s = 400.0
        k_t = 0.6
        f_ct_eff = 2.5
        rho_p_eff = 0.02
        e_s = 200000.0
        e_cm = 30000.0

        # Object to test
        formula = Form7Dot9EpsilonSmMinusEpsilonCm(
            sigma_s=sigma_s,
            k_t=k_t,
            f_ct_eff=f_ct_eff,
            rho_p_eff=rho_p_eff,
            e_s=e_s,
            e_cm=e_cm,
        )

        # Expected result, manually calculated
        manually_calculated_result = 0.001575  # dimensionless

        assert formula == pytest.approx(manually_calculated_result, rel=1e-3)

    @pytest.mark.parametrize(
        ("sigma_s", "k_t", "f_ct_eff", "rho_p_eff", "e_s", "e_cm"),
        [
            (-400.0, 0.6, 2.5, 0.02, 200000.0, 30000.0),  # sigma_s is negative
            (400.0, -0.6, 2.5, 0.02, 200000.0, 30000.0),  # k_t is negative
            (400.0, 0.6, -2.5, 0.02, 200000.0, 30000.0),  # f_ct_eff is negative
            (400.0, 0.6, 2.5, -0.02, 200000.0, 30000.0),  # rho_p_eff is negative
            (400.0, 0.6, 2.5, 0.02, -200000.0, 30000.0),  # e_s is negative
            (400.0, 0.6, 2.5, 0.02, 200000.0, -30000.0),  # e_cm is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(
        self, sigma_s: float, k_t: float, f_ct_eff: float, rho_p_eff: float, e_s: float, e_cm: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot9EpsilonSmMinusEpsilonCm(
                sigma_s=sigma_s,
                k_t=k_t,
                f_ct_eff=f_ct_eff,
                rho_p_eff=rho_p_eff,
                e_s=e_s,
                e_cm=e_cm,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\epsilon_{sm} - \epsilon_{cm} = \max\left(\frac{\sigma_s - k_t \cdot \frac{f_{ct,eff}}{\rho_{p,eff}} "
                r"\cdot \left(1 + \frac{E_s}{E_{cm}} \cdot \rho_{p,eff}\right)}{E_s}; \frac{0.6 \cdot \sigma_s}{E_s}\right)"
                r" = \max\left(\frac{400.000 - 0.600 \cdot \frac{2.500}{0.020} \cdot \left(1 + \frac{200000.000}{30000.000} "
                r"\cdot 0.020\right)}{200000.000}; \frac{0.6 \cdot 400.000}{200000.000}\right) = 0.001575 \ -",
            ),
            ("short", r"\epsilon_{sm} - \epsilon_{cm} = 0.001575 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_s = 400.0
        k_t = 0.6
        f_ct_eff = 2.5
        rho_p_eff = 0.02
        e_s = 200000.0
        e_cm = 30000.0

        # Object to test
        latex = Form7Dot9EpsilonSmMinusEpsilonCm(
            sigma_s=sigma_s,
            k_t=k_t,
            f_ct_eff=f_ct_eff,
            rho_p_eff=rho_p_eff,
            e_s=e_s,
            e_cm=e_cm,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
