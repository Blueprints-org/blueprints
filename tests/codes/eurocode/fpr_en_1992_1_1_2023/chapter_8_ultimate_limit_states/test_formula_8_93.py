"""Testing formula 8.93 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_93 import (
    Form8Dot93DesignPunchingShearStressFromDetailedAnalysis,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot93DesignPunchingShearStressFromDetailedAnalysis:
    """Validation for formula 8.93 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 250.0
        d_v = 200.0

        # Object to test
        formula = Form8Dot93DesignPunchingShearStressFromDetailedAnalysis(v_ed=v_ed, d_v=d_v)

        # Expected result, manually calculated
        manually_calculated_result = 1.25  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "d_v"),
        [
            (-250.0, 200.0),  # v_ed is negative
            (250.0, -200.0),  # d_v is negative
            (250.0, 0.0),  # d_v is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, d_v: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot93DesignPunchingShearStressFromDetailedAnalysis(v_ed=v_ed, d_v=d_v)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"\tau_{Ed} = \frac{v_{Ed}}{d_v} = \frac{250.000}{200.000} = 1.250 \ MPa"),
            ("complete_with_units", r"\tau_{Ed} = \frac{v_{Ed}}{d_v} = \frac{250.000 \ N/mm}{200.000 \ mm} = 1.250 \ MPa"),
            ("short", r"\tau_{Ed} = 1.250 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 250.0
        d_v = 200.0

        # Object to test
        latex = Form8Dot93DesignPunchingShearStressFromDetailedAnalysis(v_ed=v_ed, d_v=d_v).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
