"""Testing formula 8.91 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_91 import Form8Dot91ShearResistingEffectiveDepth
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot91ShearResistingEffectiveDepth:
    """Validation for formula 8.91 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d_vx = 210.0
        d_vy = 190.0

        # Object to test
        formula = Form8Dot91ShearResistingEffectiveDepth(d_vx=d_vx, d_vy=d_vy)

        # Expected result, manually calculated
        manually_calculated_result = 200.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d_vx", "d_vy"),
        [
            (-210.0, 190.0),  # d_vx is negative
            (0.0, 190.0),  # d_vx is zero
            (210.0, -190.0),  # d_vy is negative
            (210.0, 0.0),  # d_vy is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d_vx: float, d_vy: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot91ShearResistingEffectiveDepth(d_vx=d_vx, d_vy=d_vy)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"d_v = \frac{d_{vx} + d_{vy}}{2} = \frac{210.000 + 190.000}{2} = 200.000 \ mm"),
            ("complete_with_units", r"d_v = \frac{d_{vx} + d_{vy}}{2} = \frac{210.000 \ mm + 190.000 \ mm}{2} = 200.000 \ mm"),
            ("short", r"d_v = 200.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_vx = 210.0
        d_vy = 190.0

        # Object to test
        latex = Form8Dot91ShearResistingEffectiveDepth(d_vx=d_vx, d_vy=d_vy).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
