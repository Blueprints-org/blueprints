"""Testing formula 8.97 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_97 import (
    Form8Dot97ReplacementEffectiveDepth,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot97ReplacementEffectiveDepth:
    """Validation for formula 8.97 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_p = 800.0
        d_v = 200.0

        # Object to test
        formula = Form8Dot97ReplacementEffectiveDepth(a_p=a_p, d_v=d_v)

        # Expected result, manually calculated
        manually_calculated_result = 141.421356  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_p", "d_v"),
        [
            (-800.0, 200.0),  # a_p is negative
            (800.0, -200.0),  # d_v is negative
            (800.0, 0.0),  # d_v is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_p: float, d_v: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot97ReplacementEffectiveDepth(a_p=a_p, d_v=d_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_{pd} = \sqrt{\frac{a_p}{8} \cdot d_v} = \sqrt{\frac{800.000}{8} \cdot 200.000} = 141.421 \ mm",
            ),
            (
                "complete_with_units",
                r"a_{pd} = \sqrt{\frac{a_p}{8} \cdot d_v} = \sqrt{\frac{800.000 \ mm}{8} \cdot 200.000 \ mm} = 141.421 \ mm",
            ),
            ("short", r"a_{pd} = 141.421 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_p = 800.0
        d_v = 200.0

        # Object to test
        latex = Form8Dot97ReplacementEffectiveDepth(a_p=a_p, d_v=d_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
