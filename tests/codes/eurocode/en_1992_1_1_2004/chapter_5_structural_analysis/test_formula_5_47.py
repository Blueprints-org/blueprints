"""Testing formula 5.47 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_47 import (
    Form5Dot47UpperCharacteristicPrestressingValue,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot47UpperCharacteristicPrestressingValue:
    """Validation for formula 5.47 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        r_sup = 1.05
        p_m_t = 100.0

        # Object to test
        formula = Form5Dot47UpperCharacteristicPrestressingValue(r_sup=r_sup, p_m_t=p_m_t)

        # Expected result, manually calculated
        manually_calculated_result = 105.0

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("r_sup", "p_m_t"),
        [
            (-1.05, 100.0),  # r_sup is negative
            (1.05, -100.0),  # p_m_t is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, r_sup: float, p_m_t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot47UpperCharacteristicPrestressingValue(r_sup=r_sup, p_m_t=p_m_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"P_{k,sup} = r_{sup} \cdot P_{m,t}(x) = 1.050 \cdot 100.000 = 105.000 \ kN",
            ),
            ("short", r"P_{k,sup} = 105.000 \ kN"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        r_sup = 1.05
        p_m_t = 100.0

        # Object to test
        latex = Form5Dot47UpperCharacteristicPrestressingValue(r_sup=r_sup, p_m_t=p_m_t).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
