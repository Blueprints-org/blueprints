"""Testing formula 8.96 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_96 import (
    Form8Dot96PunchingShearGradientEnhancementCoefficient,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot96PunchingShearGradientEnhancementCoefficient:
    """Validation for formula 8.96 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the expression governs."""
        # Example values
        b_0 = 1500.0
        b_0_5 = 2400.0

        # Object to test
        formula = Form8Dot96PunchingShearGradientEnhancementCoefficient(b_0=b_0, b_0_5=b_0_5)

        # Expected result, manually calculated
        manually_calculated_result = 2.204541  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_lower_bound_governs(self) -> None:
        """Tests the evaluation of the result when the lower bound of 1 governs."""
        # Example values, with b_0 close enough to b_0_5 for the expression to fall below 1
        formula = Form8Dot96PunchingShearGradientEnhancementCoefficient(b_0=2350.0, b_0_5=2400.0)

        # Expected result, manually calculated: the expression yields 0.519615, so the lower bound governs
        manually_calculated_result = 1.0  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_upper_bound_governs(self) -> None:
        """Tests the evaluation of the result when the upper bound of 2.5 governs."""
        # Example values, with b_0 small compared to b_0_5 for the expression to exceed 2.5
        formula = Form8Dot96PunchingShearGradientEnhancementCoefficient(b_0=100.0, b_0_5=2400.0)

        # Expected result, manually calculated: the expression yields 3.524202, so the upper bound governs
        manually_calculated_result = 2.5  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("b_0", "b_0_5"),
        [
            (-1500.0, 2400.0),  # b_0 is negative
            (1500.0, -2400.0),  # b_0_5 is negative
            (1500.0, 0.0),  # b_0_5 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, b_0: float, b_0_5: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot96PunchingShearGradientEnhancementCoefficient(b_0=b_0, b_0_5=b_0_5)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"k_{pb} = \min\left(\max\left(3.6 \cdot \sqrt{1 - \frac{b_0}{b_{0,5}}}, 1\right), 2.5\right) = "
                    r"\min\left(\max\left(3.6 \cdot \sqrt{1 - \frac{1500.000}{2400.000}}, 1\right), 2.5\right) = 2.205 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"k_{pb} = \min\left(\max\left(3.6 \cdot \sqrt{1 - \frac{b_0}{b_{0,5}}}, 1\right), 2.5\right) = "
                    r"\min\left(\max\left(3.6 \cdot \sqrt{1 - \frac{1500.000 \ mm}{2400.000 \ mm}}, 1\right), 2.5\right) = 2.205 \ -"
                ),
            ),
            ("short", r"k_{pb} = 2.205 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        b_0 = 1500.0
        b_0_5 = 2400.0

        # Object to test
        latex = Form8Dot96PunchingShearGradientEnhancementCoefficient(b_0=b_0, b_0_5=b_0_5).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
