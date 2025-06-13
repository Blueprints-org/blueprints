"""Testing formula 5.6 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_6 import Form5Dot6ProjectedShearArea
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot6ProjectedShearArea:
    """Validation for formula 5.6 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        h = 500  # MM
        t_f = 20  # MM
        t_w = 10  # MM

        form = Form5Dot6ProjectedShearArea(h=h, t_f=t_f, t_w=t_w)

        # Expected result, manually calculated
        expected = 4800

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("h", "t_f", "t_w"),
        [
            (500, -20, 10),  # tf is negative
            (500, 0, 10),  # tf is zero
            (500, 20, -10),  # tw is negative
            (500, 20, 0),  # tw is zero
            (0, 20, 10),  # h is zero
            (-500, 20, 10),  # h is negative
        ],
    )
    def test_raise_error_when_negative_or_zero_values_are_given(self, h: float, t_f: float, t_w: float) -> None:
        """Test a zero and negative value for parameters h, tf, and tw."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot6ProjectedShearArea(h=h, t_f=t_f, t_w=t_w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"A_v = t_w \left(h - t_f \right) = 10 \cdot \left(500 - 20 \right) = 4800.00",
            ),
            ("short", r"A_v = 4800.00"),
            (
                "string",
                r"A_v = t_w \left(h - t_f \right) = 10 \cdot \left(500 - 20 \right) = 4800.00",
            ),
        ],
    )
    def test_latex_output(self, representation: str, expected: str) -> None:
        """Test the latex implementation."""
        # Example values
        h = 500  # MM
        t_f = 20  # MM
        t_w = 10  # MM

        form = Form5Dot6ProjectedShearArea(h=h, t_f=t_f, t_w=t_w).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected, f"{representation} representation failed."
