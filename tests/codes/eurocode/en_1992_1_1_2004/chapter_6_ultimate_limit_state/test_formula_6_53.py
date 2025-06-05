"""Testing formula 6.53 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_53 import Form6Dot53CheckPunchingShear
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot53CheckPunchingShear:
    """Validation for formula 6.53 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        beta = 1.1
        v_ed = 500.0
        u_0 = 400.0
        d = 200.0
        v_rd_max = 2.5

        # Object to test
        formula = Form6Dot53CheckPunchingShear(beta=beta, v_ed=v_ed, u_0=u_0, d=d, v_rd_max=v_rd_max)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("beta", "v_ed", "u_0", "d", "v_rd_max"),
        [
            (-1.1, 500.0, 400.0, 200.0, 2.5),  # beta is negative
            (1.1, -500.0, 400.0, 200.0, 2.5),  # v_ed is negative
            (1.1, 500.0, -400.0, 200.0, 2.5),  # u_0 is negative
            (1.1, 500.0, 400.0, -200.0, 2.5),  # d is negative
            (1.1, 500.0, 400.0, 200.0, -2.5),  # v_rd_max is negative
            (1.1, 500.0, 0.0, 200.0, 2.5),  # u_0 is zero
            (1.1, 500.0, 400.0, 0.0, 2.5),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta: float, v_ed: float, u_0: float, d: float, v_rd_max: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot53CheckPunchingShear(beta=beta, v_ed=v_ed, u_0=u_0, d=d, v_rd_max=v_rd_max)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \frac{\beta \cdot V_{Ed}}{u_{0} \cdot d} \leq v_{Rd,max} \to "
                r"\frac{1.100 \cdot 500.000}{400.000 \cdot 200.000} \leq 2.500 \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta = 1.1
        v_ed = 500.0
        u_0 = 400.0
        d = 200.0
        v_rd_max = 2.5

        # Object to test
        latex = Form6Dot53CheckPunchingShear(beta=beta, v_ed=v_ed, u_0=u_0, d=d, v_rd_max=v_rd_max).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
