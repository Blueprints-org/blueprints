"""Testing formula 8.14 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_14 import (
    Form8Dot14DesignPlasticRestistanceGrossCrossSection,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot14DesignPlasticRestistanceGrossCrossSection:
    """Validation for formula 8.14 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a = 5000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        formula = Form8Dot14DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=gamma_m0)

        # Expected result, manually calculated
        manually_calculated_result = 1775000.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a", "f_y", "gamma_m0"),
        [
            (-5000.0, 355.0, 1.0),  # a is negative
            (5000.0, -355.0, 1.0),  # f_y is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, a: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot14DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=gamma_m0)

    @pytest.mark.parametrize(
        ("a", "f_y", "gamma_m0"),
        [
            (5000.0, 355.0, 0.0),  # gamma_m0 is zero
            (5000.0, 355.0, -1.0),  # gamma_m0 is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, a: float, f_y: float, gamma_m0: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot14DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=gamma_m0)

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
        a = 5000.0
        f_y = 355.0
        gamma_m0 = 1.0

        # Object to test
        latex = Form8Dot14DesignPlasticRestistanceGrossCrossSection(a=a, f_y=f_y, gamma_m0=gamma_m0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
