"""Testing formula 6.49 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_49 import Form6Dot49AppliedPunchingShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot49AppliedPunchingShearStress:
    """Validation for formula 6.49 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed_red = 1000000.0
        u = 200.0
        d = 300.0

        # Object to test
        formula = Form6Dot49AppliedPunchingShearStress(v_ed_red=v_ed_red, u=u, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 16.6667  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_red", "u", "d"),
        [
            (-1000000.0, 200.0, 300.0),  # v_ed_red is negative
            (1000000.0, -200.0, 300.0),  # u is negative
            (1000000.0, 200.0, -300.0),  # d is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed_red: float, u: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot49AppliedPunchingShearStress(v_ed_red=v_ed_red, u=u, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Ed} = \frac{V_{Ed,red}}{u \cdot d} = \frac{1000000.000}{200.000 \cdot 300.000} = 16.667 \ MPa",
            ),
            ("short", r"v_{Ed} = 16.667 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_red = 1000000.0
        u = 200.0
        d = 300.0

        # Object to test
        latex = Form6Dot49AppliedPunchingShearStress(v_ed_red=v_ed_red, u=u, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
