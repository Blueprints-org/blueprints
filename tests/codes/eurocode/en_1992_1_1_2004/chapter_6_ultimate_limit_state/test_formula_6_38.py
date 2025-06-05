"""Testing formula 6.38 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_38 import Form6Dot38MaxShearStress
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot38MaxShearStress:
    """Validation for formula 6.38 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        beta = 1.2
        v_ed = 500.0
        u_i = 300.0
        d = 200.0

        # Object to test
        formula = Form6Dot38MaxShearStress(beta=beta, v_ed=v_ed, u_i=u_i, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.01  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("beta", "v_ed", "u_i", "d"),
        [
            (-1.2, 500.0, 300.0, 200.0),  # beta is negative
            (1.2, -500.0, 300.0, 200.0),  # v_ed is negative
            (1.2, 500.0, -300.0, 200.0),  # u_i is negative
            (1.2, 500.0, 300.0, -200.0),  # d is negative
            (1.2, 500.0, 0.0, 200.0),  # u_i is zero
            (1.2, 500.0, 300.0, 0.0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta: float, v_ed: float, u_i: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot38MaxShearStress(beta=beta, v_ed=v_ed, u_i=u_i, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Ed} = \beta \cdot \frac{V_{Ed}}{u_{i} \cdot d} = 1.200 \cdot \frac{500.000}{300.000 \cdot 200.000} = 0.010 \ MPa",
            ),
            ("short", r"v_{Ed} = 0.010 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta = 1.2
        v_ed = 500.0
        u_i = 300.0
        d = 200.0

        # Object to test
        latex = Form6Dot38MaxShearStress(beta=beta, v_ed=v_ed, u_i=u_i, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
