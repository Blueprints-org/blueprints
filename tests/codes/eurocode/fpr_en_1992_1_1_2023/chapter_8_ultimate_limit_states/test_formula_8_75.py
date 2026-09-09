"""Testing formula 8.75 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_75 import (
    Form8Dot75LongitudinalShearStressDueToCompositeAction,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot75LongitudinalShearStressDueToCompositeAction:
    """Validation for formula 8.75 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        beta_new = 0.45
        v_ed = 500000.0
        z = 450.0
        b_i = 500.0

        # Object to test
        formula = Form8Dot75LongitudinalShearStressDueToCompositeAction(beta_new=beta_new, v_ed=v_ed, z=z, b_i=b_i)

        # Expected result, manually calculated: 0.45 * 500000 / (450 * 500)
        manually_calculated_result = 1.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("beta_new", "v_ed", "z", "b_i"),
        [
            (-0.45, 500000.0, 450.0, 500.0),  # beta_new is negative
            (0.45, -500000.0, 450.0, 500.0),  # v_ed is negative
            (0.45, 500000.0, -450.0, 500.0),  # z is negative
            (0.45, 500000.0, 0.0, 500.0),  # z is zero
            (0.45, 500000.0, 450.0, -500.0),  # b_i is negative
            (0.45, 500000.0, 450.0, 0.0),  # b_i is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta_new: float, v_ed: float, z: float, b_i: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot75LongitudinalShearStressDueToCompositeAction(beta_new=beta_new, v_ed=v_ed, z=z, b_i=b_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Edi} = \frac{\beta_{new} \cdot V_{Ed}}{z \cdot b_i} = \frac{0.450 \cdot 500000.000}{450.000 \cdot 500.000} = 1.000 \ MPa",
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Edi} = \frac{\beta_{new} \cdot V_{Ed}}{z \cdot b_i} = "
                    r"\frac{0.450 \cdot 500000.000 \ N}{450.000 \ mm \cdot 500.000 \ mm} = 1.000 \ MPa"
                ),
            ),
            ("short", r"\tau_{Edi} = 1.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta_new = 0.45
        v_ed = 500000.0
        z = 450.0
        b_i = 500.0

        # Object to test
        latex = Form8Dot75LongitudinalShearStressDueToCompositeAction(beta_new=beta_new, v_ed=v_ed, z=z, b_i=b_i).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
