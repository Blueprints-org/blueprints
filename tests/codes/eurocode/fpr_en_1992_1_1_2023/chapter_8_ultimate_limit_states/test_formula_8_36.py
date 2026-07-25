"""Testing formula 8.36 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_36 import (
    Form8Dot36EffectiveDepthPrestressedMembers,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot36EffectiveDepthPrestressedMembers:
    """Validation for formula 8.36 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d_s = 500.0
        a_s = 1500.0
        d_p = 450.0
        a_p = 800.0

        # Object to test
        formula = Form8Dot36EffectiveDepthPrestressedMembers(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p)

        # Expected result, manually calculated
        manually_calculated_result = 483.783784  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_prestressed_reinforcement_is_omitted(self) -> None:
        """Tests the omission of the prestressed reinforcement allowed by 8.2.2(6), which returns the effective depth
        of the longitudinal tension reinforcement.
        """
        formula = Form8Dot36EffectiveDepthPrestressedMembers(d_s=500.0, a_s=1500.0, d_p=450.0, a_p=0.0)

        assert formula == pytest.approx(expected=500.0, rel=1e-9)

    @pytest.mark.parametrize(
        ("d_s", "a_s", "d_p", "a_p"),
        [
            (-500.0, 1500.0, 450.0, 800.0),  # d_s is negative
            (500.0, -1500.0, 450.0, 800.0),  # a_s is negative
            (500.0, 1500.0, -450.0, 800.0),  # d_p is negative
            (500.0, 1500.0, 450.0, -800.0),  # a_p is negative
            (500.0, 0.0, 450.0, 0.0),  # no reinforcement at all, so the denominator is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d_s: float, a_s: float, d_p: float, a_p: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot36EffectiveDepthPrestressedMembers(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"d = \frac{\left(d_s\right)^2 \cdot A_s + \left(d_p\right)^2 \cdot A_p}{d_s \cdot A_s + d_p \cdot A_p} = "
                r"\frac{\left(500.000\right)^2 \cdot 1500.000 + \left(450.000\right)^2 \cdot 800.000}"
                r"{500.000 \cdot 1500.000 + 450.000 \cdot 800.000} = 483.784 \ mm",
            ),
            (
                "complete_with_units",
                r"d = \frac{\left(d_s\right)^2 \cdot A_s + \left(d_p\right)^2 \cdot A_p}{d_s \cdot A_s + d_p \cdot A_p} = "
                r"\frac{\left(500.000 \ mm\right)^2 \cdot 1500.000 \ mm^2 + \left(450.000 \ mm\right)^2 \cdot 800.000 \ mm^2}"
                r"{500.000 \ mm \cdot 1500.000 \ mm^2 + 450.000 \ mm \cdot 800.000 \ mm^2} = 483.784 \ mm",
            ),
            ("short", r"d = 483.784 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_s = 500.0
        a_s = 1500.0
        d_p = 450.0
        a_p = 800.0

        # Object to test
        latex = Form8Dot36EffectiveDepthPrestressedMembers(d_s=d_s, a_s=a_s, d_p=d_p, a_p=a_p).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
