"""Testing formula 6.32 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_32 import Form6Dot32EffectiveDepthSlab
from blueprints.validations import NegativeValueError


class TestForm6Dot32EffectiveDepthSlab:
    """Validation for formula 6.32 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d_y = 200.0
        d_z = 300.0

        # Object to test
        formula = Form6Dot32EffectiveDepthSlab(d_y=d_y, d_z=d_z)

        # Expected result, manually calculated
        manually_calculated_result = 250.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d_y", "d_z"),
        [
            (-200.0, 300.0),  # d_y is negative
            (200.0, -300.0),  # d_z is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, d_y: float, d_z: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot32EffectiveDepthSlab(d_y=d_y, d_z=d_z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"d_{eff} = \frac{d_{y} + d_{z}}{2} = \frac{200.000 + 300.000}{2} = 250.000 \ mm",
            ),
            ("short", r"d_{eff} = 250.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d_y = 200.0
        d_z = 300.0

        # Object to test
        latex = Form6Dot32EffectiveDepthSlab(d_y=d_y, d_z=d_z).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
