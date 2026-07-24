"""Testing formula 8.19 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_19 import Form8Dot19AverageShearStressPlanarMembers
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot19AverageShearStressPlanarMembers:
    """Validation for formula 8.19 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 250.0
        z = 450.0

        # Object to test
        formula = Form8Dot19AverageShearStressPlanarMembers(v_ed=v_ed, z=z)

        # Expected result, manually calculated
        manually_calculated_result = 0.555556  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "z"),
        [
            (-250.0, 450.0),  # v_ed is negative
            (250.0, -450.0),  # z is negative
            (250.0, 0.0),  # z is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, z: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot19AverageShearStressPlanarMembers(v_ed=v_ed, z=z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Ed} = \frac{v_{Ed}}{z} = \frac{250.000}{450.000} = 0.556 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Ed} = \frac{v_{Ed}}{z} = \frac{250.000 \ N/mm}{450.000 \ mm} = 0.556 \ MPa",
            ),
            ("short", r"\tau_{Ed} = 0.556 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 250.0
        z = 450.0

        # Object to test
        latex = Form8Dot19AverageShearStressPlanarMembers(v_ed=v_ed, z=z).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
