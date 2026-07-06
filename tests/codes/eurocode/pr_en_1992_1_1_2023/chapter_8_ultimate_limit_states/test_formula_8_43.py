"""Testing formula 8.43 of prEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.pr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_43 import (
    Form8Dot43ShearReinforcementRatio,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot43ShearReinforcementRatio:
    """Validation for formula 8.43 from prEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw = 226.19  # mm²
        b_w = 500.0  # mm
        s = 150.0  # mm

        # Object to test
        formula = Form8Dot43ShearReinforcementRatio(a_sw=a_sw, b_w=b_w, s=s)

        # Expected result, manually calculated
        manually_calculated_result = 0.003016  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-3)

    @pytest.mark.parametrize(
        ("a_sw", "b_w", "s"),
        [
            (-226.19, 500.0, 150.0),  # a_sw is negative
        ],
    )
    def test_raise_error_when_negative_a_sw_is_given(self, a_sw: float, b_w: float, s: float) -> None:
        """Test invalid values for a_sw."""
        with pytest.raises(NegativeValueError):
            Form8Dot43ShearReinforcementRatio(a_sw=a_sw, b_w=b_w, s=s)

    @pytest.mark.parametrize(
        ("a_sw", "b_w", "s"),
        [
            (226.19, 0.0, 150.0),  # b_w is zero
            (226.19, -500.0, 150.0),  # b_w is negative
            (226.19, 500.0, 0.0),  # s is zero
            (226.19, 500.0, -150.0),  # s is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sw: float, b_w: float, s: float) -> None:
        """Test invalid values for b_w and s."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot43ShearReinforcementRatio(a_sw=a_sw, b_w=b_w, s=s)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_w = \frac{A_{sw}}{b_w \cdot s} = \frac{226.190}{500.000 \cdot 150.000} = 0.003",
            ),
            (
                "complete_with_units",
                r"\rho_w = \frac{A_{sw}}{b_w \cdot s} = \frac{226.190 \ mm^2}{500.000 \ mm \cdot 150.000 \ mm} = 0.003",
            ),
            ("short", r"\rho_w = 0.003"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw = 226.19  # mm²
        b_w = 500.0  # mm
        s = 150.0  # mm

        # Object to test
        latex = Form8Dot43ShearReinforcementRatio(a_sw=a_sw, b_w=b_w, s=s).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
