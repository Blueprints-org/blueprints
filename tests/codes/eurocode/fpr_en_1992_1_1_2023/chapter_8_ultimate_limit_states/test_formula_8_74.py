"""Testing formula 8.74 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_74 import Form8Dot74DesignShearStressAtInterface
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot74DesignShearStressAtInterface:
    """Validation for formula 8.74 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_edi = 200000.0
        a_i = 250000.0

        # Object to test
        formula = Form8Dot74DesignShearStressAtInterface(v_edi=v_edi, a_i=a_i)

        # Expected result, manually calculated: 200000 / 250000
        manually_calculated_result = 0.8  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_edi", "a_i"),
        [
            (-200000.0, 250000.0),  # v_edi is negative
            (200000.0, -250000.0),  # a_i is negative
            (200000.0, 0.0),  # a_i is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_edi: float, a_i: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot74DesignShearStressAtInterface(v_edi=v_edi, a_i=a_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"\tau_{Edi} = \frac{V_{Edi}}{A_i} = \frac{200000.000}{250000.000} = 0.800 \ MPa"),
            ("complete_with_units", r"\tau_{Edi} = \frac{V_{Edi}}{A_i} = \frac{200000.000 \ N}{250000.000 \ mm^2} = 0.800 \ MPa"),
            ("short", r"\tau_{Edi} = 0.800 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_edi = 200000.0
        a_i = 250000.0

        # Object to test
        latex = Form8Dot74DesignShearStressAtInterface(v_edi=v_edi, a_i=a_i).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
