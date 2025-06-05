"""Testing formula 7.19 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_19 import Form7Dot19DistributionCoefficient
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot19DistributionCoefficient:
    """Validation for formula 7.19 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        beta = 0.5
        sigma_sr = 200.0
        sigma_s = 400.0

        # Object to test
        formula = Form7Dot19DistributionCoefficient(beta=beta, sigma_sr=sigma_sr, sigma_s=sigma_s)

        # Expected result, manually calculated
        manually_calculated_result = 0.875  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("beta", "sigma_sr", "sigma_s"),
        [
            (-0.5, 200.0, 400.0),  # beta is negative
            (0.5, -200.0, 400.0),  # sigma_sr is negative
            (0.5, 200.0, -400.0),  # sigma_s is negative
            (0.5, 200.0, 0.0),  # sigma_s is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta: float, sigma_sr: float, sigma_s: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot19DistributionCoefficient(beta=beta, sigma_sr=sigma_sr, sigma_s=sigma_s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\zeta = 1 - \beta \left(\frac{\sigma_{sr}}{\sigma_{s}}\right)^2 = "
                r"1 - 0.500 \left(\frac{200.000}{400.000}\right)^2 = 0.875 \ -",
            ),
            ("short", r"\zeta = 0.875 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta = 0.5
        sigma_sr = 200.0
        sigma_s = 400.0

        # Object to test
        latex = Form7Dot19DistributionCoefficient(beta=beta, sigma_sr=sigma_sr, sigma_s=sigma_s).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
