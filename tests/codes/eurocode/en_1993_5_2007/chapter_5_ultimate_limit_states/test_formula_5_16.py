"""Testing formula 5.16 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_16 import Form5Dot16PlasticDesignResistance
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot16PlasticDesignResistance:
    """Validation for formula 5.16 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        a = 5000  # MM2
        f_y = 355  # MPA
        gamma_m0 = 1.0  # DIMENSIONLESS

        # Object to test
        formula = Form5Dot16PlasticDesignResistance(a=a, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 1775000.0  # N

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "f_y", "gamma_m0"),
        [
            (-5000, 355, 1.0),  # a is negative
            (5000, -355, 1.0),  # f_y is negative
            (5000, 355, -1.0),  # gamma_m0 is negative
            (5000, 355, 0),  # gamma_m0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises((LessOrEqualToZeroError, NegativeValueError)):
            Form5Dot16PlasticDesignResistance(a=a, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{pl,Rd} = \frac{A \cdot f_y}{\gamma_{M0}} = \frac{5000.000 \cdot 355.000}{1.000} = 1775000.000 \ N",
            ),
            ("short", r"N_{pl,Rd} = 1775000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a = 5000  # MM2
        f_y = 355  # MPA
        gamma_m0 = 1.0  # DIMENSIONLESS

        # Object to test
        latex = Form5Dot16PlasticDesignResistance(a=a, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
