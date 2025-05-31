"""Testing formula 6.54 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_54 import Form6Dot54ControlPerimeter
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot54ControlPerimeter:
    """Validation for formula 6.54 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        beta = 1.1
        v_ed = 200.0
        v_rd_c = 1.5
        d = 500.0

        # Object to test
        formula = Form6Dot54ControlPerimeter(beta=beta, v_ed=v_ed, v_rd_c=v_rd_c, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 0.293333333333333  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("beta", "v_ed", "v_rd_c", "d"),
        [
            (-1.1, 200.0, 1.5, 500.0),  # beta is negative
            (1.1, -200.0, 1.5, 500.0),  # v_ed is negative
            (1.1, 200.0, -1.5, 500.0),  # v_rd_c is negative
            (1.1, 200.0, 1.5, -500.0),  # d is negative
            (1.1, 200.0, 0, 500.0),  # v_rd_c is zero
            (1.1, 200.0, 1.5, 0),  # d is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, beta: float, v_ed: float, v_rd_c: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot54ControlPerimeter(beta=beta, v_ed=v_ed, v_rd_c=v_rd_c, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"u_{out,ef} = \frac{\beta \cdot V_{Ed}}{v_{Rd,c} \cdot d} = \frac{1.100 \cdot 200.000}{1.500 \cdot 500.000} = 0.293 \ mm",
            ),
            ("short", r"u_{out,ef} = 0.293 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        beta = 1.1
        v_ed = 200.0
        v_rd_c = 1.5
        d = 500.0

        # Object to test
        latex = Form6Dot54ControlPerimeter(beta=beta, v_ed=v_ed, v_rd_c=v_rd_c, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
