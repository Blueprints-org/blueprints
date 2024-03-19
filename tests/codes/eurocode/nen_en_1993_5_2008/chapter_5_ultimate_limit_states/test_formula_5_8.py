"""Testing formula 5.8 of NEN-EN 1993-5:2008."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states.formula_5_8 import Form5Dot8RelativeSlenderness
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot8RelativeSlenderness:
    """Validation for formula 5.8 from NEN-EN 1993-5:2008."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c = 500  # MM
        t_w = 10  # MM
        f_y = 250  # MPA
        e = 200000  # MPA

        form = Form5Dot8RelativeSlenderness(c=c, t_w=t_w, f_y=f_y, e=e)

        # Expected result, manually calculated
        expected = 0.611647366

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("c", "t_w", "f_y", "e"),
        [
            (500, -10, 250, 200000),  # t_w is negative
            (500, 0, 250, 200000),  # t_w is zero
            (500, 10, -250, 200000),  # f_y is negative
            (500, 10, 0, 200000),  # f_y is zero
            (500, 10, 250, -200000),  # E is negative
            (500, 10, 250, 0),  # E is zero
        ],
    )
    def test_raise_error_when_negative_or_zero_values_are_given(self, c: float, t_w: float, f_y: float, e: float) -> None:
        """Test a zero and negative value for parameters c, t_w, f_y, and e."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot8RelativeSlenderness(c=c, t_w=t_w, f_y=f_y, e=e)

    def test_latex_output(self) -> None:
        """Test the latex implementation."""
        c = 500  # MM
        t_w = 10  # MM
        f_y = 250  # MPA
        e = 200000  # MPA

        form = Form5Dot8RelativeSlenderness(c=c, t_w=t_w, f_y=f_y, e=e)
        assert (
            form.latex().complete
            == r"\overline{\lambda} = 0.346 \cdot \frac{c}{t_w} \sqrt{\frac{f_y}{E}} = 0.346 \cdot \frac{500}{10} \sqrt{\frac{250}{200000}} = "
            + str(form)
        )
        assert form.latex().short == r"\overline{\lambda} = " + str(form)
        assert str(
            form.latex()
        ) == r"\overline{\lambda} = 0.346 \cdot \frac{c}{t_w} \sqrt{\frac{f_y}{E}} = 0.346 \cdot \frac{500}{10} \sqrt{\frac{250}{200000}} = " + str(
            form
        )
