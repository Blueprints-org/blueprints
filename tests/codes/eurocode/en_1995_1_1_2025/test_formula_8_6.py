"""Testing formula 8.6 of EN 1995-1-1:2025."""

import pytest

from blueprints.codes.eurocode.en_1995_1_1_2025.formula_8_6 import Form8Dot6DesignCompressiveStressPerpendicularToGrain
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot6DesignCompressiveStressPerpendicularToGrain:
    """Validation for formula 8.6 from EN 1995-1-1:2025."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        capital_f_90_d = 10000.0  # N
        a = 2000.0  # mm^2

        # Object to test
        formula = Form8Dot6DesignCompressiveStressPerpendicularToGrain(capital_f_90_d=capital_f_90_d, a=a)

        # Expected result, manually calculated
        manually_calculated_result = 5.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("capital_f_90_d", "a"),
        [
            (-10000.0, 2000.0),  # capital_f_90_d is negative
        ],
    )
    def test_raise_error_when_negative_value_is_given(self, capital_f_90_d: float, a: float) -> None:
        """Test negative values for capital_f_90_d."""
        with pytest.raises(NegativeValueError):
            Form8Dot6DesignCompressiveStressPerpendicularToGrain(capital_f_90_d=capital_f_90_d, a=a)

    @pytest.mark.parametrize(
        ("capital_f_90_d", "a"),
        [
            (10000.0, 0.0),  # a is zero
            (10000.0, -2000.0),  # a is negative
        ],
    )
    def test_raise_error_when_invalid_a_is_given(self, capital_f_90_d: float, a: float) -> None:
        """Test zero and negative values for a."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot6DesignCompressiveStressPerpendicularToGrain(capital_f_90_d=capital_f_90_d, a=a)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{c,90,d} = \frac{F_{c,90,d}}{A} = \frac{10000.000}{2000.000} = 5.000 \ MPa",
            ),
            (
                "complete_with_units",
                r"\sigma_{c,90,d} = \frac{F_{c,90,d}}{A} = \frac{10000.000 \, N}{2000.000 \, mm^2} = 5.000 \ MPa",
            ),
            (
                "short",
                r"\sigma_{c,90,d} = 5.000 \ MPa",
            ),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        capital_f_90_d = 10000.0
        a = 2000.0

        # Object to test
        latex = Form8Dot6DesignCompressiveStressPerpendicularToGrain(capital_f_90_d=capital_f_90_d, a=a).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
