"""Testing formula 6.48 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_48 import Form6Dot48NetAppliedPunchingForce
from blueprints.validations import NegativeValueError


class TestForm6Dot48NetAppliedPunchingForce:
    """Validation for formula 6.48 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 1000.0
        delta_v_ed = 200.0

        # Object to test
        formula = Form6Dot48NetAppliedPunchingForce(v_ed=v_ed, delta_v_ed=delta_v_ed)

        # Expected result, manually calculated
        manually_calculated_result = 800.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "delta_v_ed"),
        [
            (-1000.0, 200.0),  # v_ed is negative
            (1000.0, -200.0),  # delta_v_ed is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed: float, delta_v_ed: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot48NetAppliedPunchingForce(v_ed=v_ed, delta_v_ed=delta_v_ed)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Ed,red} = V_{Ed} - \Delta V_{Ed} = 1000.000 - 200.000 = 800.000 \ N",
            ),
            ("short", r"V_{Ed,red} = 800.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 1000.0
        delta_v_ed = 200.0

        # Object to test
        latex = Form6Dot48NetAppliedPunchingForce(v_ed=v_ed, delta_v_ed=delta_v_ed).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
