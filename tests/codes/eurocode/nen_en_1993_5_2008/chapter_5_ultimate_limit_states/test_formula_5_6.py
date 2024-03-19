"""Testing formula 5.6 of NEN-EN 1993-5:2008."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states.formula_5_6 import Form5Dot6ProjectedShearArea
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot6ProjectedShearArea:
    """Validation for formula 5.6 from NEN-EN 1993-5:2008."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        h = 500  # MM
        tf = 20  # MM
        tw = 10  # MM

        form = Form5Dot6ProjectedShearArea(h=h, tf=tf, tw=tw)

        # Expected result, manually calculated
        expected = 4800

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("h", "tf", "tw"),
        [
            (500, -20, 10),  # tf is negative
            (500, 0, 10),  # tf is zero
            (500, 20, -10),  # tw is negative
            (500, 20, 0),  # tw is zero
        ],
    )
    def test_raise_error_when_negative_or_zero_values_are_given(self, h: float, tf: float, tw: float) -> None:
        """Test a zero and negative value for parameters h, tf, and tw."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot6ProjectedShearArea(h=h, tf=tf, tw=tw)

    def test_latex_output(self) -> None:
        """Test the latex implementation."""
        h = 500  # MM
        tf = 20  # MM
        tw = 10  # MM

        form = Form5Dot6ProjectedShearArea(h=h, tf=tf, tw=tw)
        assert form.latex().complete == r"A_v = t_w \left(h - t_f \right) = 10 \cdot \left(500 - 20 \right) = " + str(form)
        assert form.latex().short == r"A_v = " + str(form)
        assert str(form.latex()) == r"A_v = t_w \left(h - t_f \right) = 10 \cdot \left(500 - 20 \right) = " + str(form)
