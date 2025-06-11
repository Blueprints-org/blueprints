"""Testing formula 5.45 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_45 import Form5Dot45LossesDueToFriction
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot45LossesDueToFriction:
    """Validation for formula 5.45 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        p_max = 1000.0
        mu = 0.2
        theta = 0.1
        k = 0.01
        x = 50.0

        # Object to test
        formula = Form5Dot45LossesDueToFriction(p_max=p_max, mu=mu, theta=theta, k=k, x=x)

        # Expected result, manually calculated
        manually_calculated_result = 113.079563283

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("p_max", "mu", "theta", "k", "x"),
        [
            (-1000.0, 0.2, 0.1, 0.01, 50.0),  # p_max is negative
            (1000.0, -0.2, 0.1, 0.01, 50.0),  # mu is negative
            (1000.0, 0.2, -0.1, 0.01, 50.0),  # theta is negative
            (1000.0, 0.2, 0.1, -0.01, 50.0),  # k is negative
            (1000.0, 0.2, 0.1, 0.01, -50.0),  # x is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, p_max: float, mu: float, theta: float, k: float, x: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot45LossesDueToFriction(p_max=p_max, mu=mu, theta=theta, k=k, x=x)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta P_{\mu}(x) = P_{max} \cdot \left( 1 - e^{-\mu \cdot (\theta + k \cdot x)} \right) = "
                r"1000.000 \cdot \left( 1 - e^{-0.200 \cdot (0.100 + 0.010 \cdot 50.000)} \right) = 113.080 \ kN",
            ),
            ("short", r"\Delta P_{\mu}(x) = 113.080 \ kN"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        p_max = 1000.0
        mu = 0.2
        theta = 0.1
        k = 0.01
        x = 50.0

        # Object to test
        latex = Form5Dot45LossesDueToFriction(p_max=p_max, mu=mu, theta=theta, k=k, x=x).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
