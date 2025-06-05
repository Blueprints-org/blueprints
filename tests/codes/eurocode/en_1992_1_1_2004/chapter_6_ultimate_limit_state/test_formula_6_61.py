"""Testing formula 6.61 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_61 import (
    Form6Dot61DesignValueCompressiveStressResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot61DesignValueCompressiveStressResistance:
    """Validation for formula 6.61 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k_2 = 0.85
        nu_prime = 0.6
        f_cd = 30.0

        # Object to test
        formula = Form6Dot61DesignValueCompressiveStressResistance(k_2=k_2, nu_prime=nu_prime, f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 15.3  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k_2", "nu_prime", "f_cd"),
        [
            (-0.85, 0.6, 30.0),  # k_2 is negative
            (0.85, -0.6, 30.0),  # nu_prime is negative
            (0.85, 0.6, -30.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k_2: float, nu_prime: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot61DesignValueCompressiveStressResistance(k_2=k_2, nu_prime=nu_prime, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{Rd,max} = k_2 \cdot \nu' \cdot f_{cd} = 0.850 \cdot 0.600 \cdot 30.000 = 15.300 \ MPa",
            ),
            ("short", r"\sigma_{Rd,max} = 15.300 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k_2 = 0.85
        nu_prime = 0.6
        f_cd = 30.0

        # Object to test
        latex = Form6Dot61DesignValueCompressiveStressResistance(k_2=k_2, nu_prime=nu_prime, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
