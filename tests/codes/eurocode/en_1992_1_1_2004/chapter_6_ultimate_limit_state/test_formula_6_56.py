"""Testing formula 6.56 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_56 import (
    Form6Dot56DesignStrengthConcreteStrussTransverseTension,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot56DesignStrengthConcreteStrussTransverseTension:
    """Validation for formula 6.56 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        nu_prime = 0.85
        f_cd = 25.0

        # Object to test
        formula = Form6Dot56DesignStrengthConcreteStrussTransverseTension(nu_prime=nu_prime, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 12.75  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("nu_prime", "f_cd"),
        [
            (-0.85, 25.0),  # nu_prime is negative
            (0.85, -25.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, nu_prime: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot56DesignStrengthConcreteStrussTransverseTension(nu_prime=nu_prime, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{Rd,max} = 0.6 \cdot \nu' \cdot f_{cd} = 0.6 \cdot 0.850 \cdot 25.000 = 12.750 \ MPa",
            ),
            ("short", r"\sigma_{Rd,max} = 12.750 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        nu_prime = 0.85
        f_cd = 25.0

        # Object to test
        latex = Form6Dot56DesignStrengthConcreteStrussTransverseTension(nu_prime=nu_prime, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
