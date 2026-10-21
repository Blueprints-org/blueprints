"""Testing formula 8.107 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_107 import Form8Dot107ShearReinforcementRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot107ShearReinforcementRatio:
    """Validation for formula 8.107 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sw = 78.5
        s_r = 150.0
        s_t = 200.0

        # Object to test
        formula = Form8Dot107ShearReinforcementRatio(a_sw=a_sw, s_r=s_r, s_t=s_t)

        # Expected result, manually calculated
        manually_calculated_result = 0.0026167  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_sw", "s_r", "s_t"),
        [
            (-78.5, 150.0, 200.0),  # a_sw is negative
            (78.5, -150.0, 200.0),  # s_r is negative
            (78.5, 0.0, 200.0),  # s_r is zero
            (78.5, 150.0, -200.0),  # s_t is negative
            (78.5, 150.0, 0.0),  # s_t is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sw: float, s_r: float, s_t: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot107ShearReinforcementRatio(a_sw=a_sw, s_r=s_r, s_t=s_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_w = \frac{A_{sw}}{s_r \cdot s_t} = \frac{78.500}{150.000 \cdot 200.000} = 0.003 \ -",
            ),
            (
                "complete_with_units",
                r"\rho_w = \frac{A_{sw}}{s_r \cdot s_t} = \frac{78.500 \ mm^2}{150.000 \ mm \cdot 200.000 \ mm} = 0.003 \ -",
            ),
            ("short", r"\rho_w = 0.003 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sw = 78.5
        s_r = 150.0
        s_t = 200.0

        # Object to test
        latex = Form8Dot107ShearReinforcementRatio(a_sw=a_sw, s_r=s_r, s_t=s_t).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
