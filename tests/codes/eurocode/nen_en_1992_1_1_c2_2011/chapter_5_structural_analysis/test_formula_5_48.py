"""Testing formula 5.48 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_48 import (
    Form5Dot48LowerCharacteristicPrestressingValue,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot48LowerCharacteristicPrestressingValue:
    """Validation for formula 5.48 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        r_inf = 0.95
        p_m_t = 100.0

        # Object to test
        formula = Form5Dot48LowerCharacteristicPrestressingValue(r_inf=r_inf, p_m_t=p_m_t)

        # Expected result, manually calculated
        manually_calculated_result = 95.0

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("r_inf", "p_m_t"),
        [
            (-0.95, 100.0),  # r_inf is negative
            (0.95, -100.0),  # p_m_t is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, r_inf: float, p_m_t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot48LowerCharacteristicPrestressingValue(r_inf=r_inf, p_m_t=p_m_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"P_{k,inf} = r_{inf} \cdot P_{m,t}(x) = 0.950 \cdot 100.000 = 95.000 \ kN",
            ),
            ("short", r"P_{k,inf} = 95.000 \ kN"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        r_inf = 0.95
        p_m_t = 100.0

        # Object to test
        latex = Form5Dot48LowerCharacteristicPrestressingValue(r_inf=r_inf, p_m_t=p_m_t).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
