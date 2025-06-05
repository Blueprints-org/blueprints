"""Testing formula 7.10 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_10 import Form7Dot10RhoPEff
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot10RhoPEff:
    """Validation for formula 7.10 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_s = 1500.0
        xi_1 = 0.7225
        a_p_prime = 1200.0
        a_c_eff = 25000.0

        # Object to test
        formula = Form7Dot10RhoPEff(a_s=a_s, xi_1=xi_1, a_p_prime=a_p_prime, a_c_eff=a_c_eff)

        # Expected result, manually calculated
        manually_calculated_result = 0.09468  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_s", "xi_1", "a_p_prime", "a_c_eff"),
        [
            (-1500.0, 0.7225, 1200.0, 25000.0),  # a_s is negative
            (1500.0, -0.7225, 1200.0, 25000.0),  # xi_1 is negative
            (1500.0, 0.7225, -1200.0, 25000.0),  # a_p_prime is negative
            (1500.0, 0.7225, 1200.0, -25000.0),  # a_c_eff is negative
            (1500.0, 0.7225, 1200.0, 0.0),  # a_c_eff is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_s: float, xi_1: float, a_p_prime: float, a_c_eff: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot10RhoPEff(a_s=a_s, xi_1=xi_1, a_p_prime=a_p_prime, a_c_eff=a_c_eff)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_{p,eff} = \frac{A_s + \xi_1 \cdot A'_p}{A_{c,eff}} = "
                r"\frac{1500.000 + 0.723 \cdot 1200.000}{25000.000} = 0.095 \ -",
            ),
            ("short", r"\rho_{p,eff} = 0.095 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_s = 1500.0
        xi_1 = 0.7225
        a_p_prime = 1200.0
        a_c_eff = 25000.0

        # Object to test
        latex = Form7Dot10RhoPEff(a_s=a_s, xi_1=xi_1, a_p_prime=a_p_prime, a_c_eff=a_c_eff).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
