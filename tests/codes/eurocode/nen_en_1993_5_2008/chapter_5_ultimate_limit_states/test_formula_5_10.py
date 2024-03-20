"""Testing formula 5.10 of NEN-EN 1993-5:2008."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states.formula_5_10 import Form5Dot10ReductionFactorShear
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot10ReductionFactorShear:
    """Validation for formula 5.10 from NEN-EN 1993-5:2008."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_ed = 100  # kN
        v_pl_rd = 400  # kN

        form = Form5Dot10ReductionFactorShear(v_ed=v_ed, v_pl_rd=v_pl_rd)

        # Expected result, manually calculated
        expected = 0.25

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_rd"),
        [
            (-100, 200),  # v_ed is negative
            (100, -200),  # v_pl_rd is negative
            (0, 200),  # v_ed is zero
            (100, 0),  # v_pl_rd is zero
        ],
    )
    def test_raise_error_when_negative_or_zero_values_are_given(self, v_ed: float, v_pl_rd: float) -> None:
        """Test a zero and negative value for parameters v_ed and v_pl_rd."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot10ReductionFactorShear(v_ed=v_ed, v_pl_rd=v_pl_rd)

    def test_latex_output(self) -> None:
        """Test the latex implementation."""
        v_ed = 100  # kN
        v_pl_rd = 200  # kN

        form = Form5Dot10ReductionFactorShear(v_ed=v_ed, v_pl_rd=v_pl_rd)
        assert (
            form.latex().complete
            == r"\rho = \left(2 \cdot \frac{V_{Ed}}{V_{pl,Rd}} - 1\right)^2 = \left(2 \cdot \frac{100}{200} - 1\right)^2 = " + str(form)
        )
        assert form.latex().short == r"\rho = " + str(form)
        assert str(
            form.latex()
        ) == r"\rho = \left(2 \cdot \frac{V_{Ed}}{V_{pl,Rd}} - 1\right)^2 = \left(2 \cdot \frac{100}{200} - 1\right)^2 = " + str(form)
