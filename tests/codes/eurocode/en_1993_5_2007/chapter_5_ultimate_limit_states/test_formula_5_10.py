"""Testing formula 5.10 of EN 1993-5:2007."""

import pytest

from blueprints.codes.eurocode.en_1993_5_2007.chapter_5_ultimate_limit_states.formula_5_10 import Form5Dot10ReductionFactorShearArea
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot10ReductionFactorShearArea:
    """Validation for formula 5.10 from EN 1993-5:2007."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        v_ed = 100  # kN
        v_pl_rd = 400  # kN

        form = Form5Dot10ReductionFactorShearArea(v_ed=v_ed, v_pl_rd=v_pl_rd)

        # Expected result, manually calculated
        expected = 0.25

        assert form == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_rd"),
        [
            (0, 200),  # v_ed is zero
            (-100, 200),  # v_ed is negative
            (100, 0),  # v_pl_rd is zero
            (100, -200),  # v_pl_rd is negative
        ],
    )
    def test_raise_error_when_negative_or_zero_values_are_given(self, v_ed: float, v_pl_rd: float) -> None:
        """Test a zero and negative value for parameters v_ed and v_pl_rd."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot10ReductionFactorShearArea(v_ed=v_ed, v_pl_rd=v_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho = \left(2 \cdot \frac{V_{Ed}}{V_{pl,Rd}} - 1\right)^2 = \left(2 \cdot \frac{100}{400} - 1\right)^2 = 0.25",
            ),
            ("short", r"\rho = 0.25"),
            (
                "string",
                r"\rho = \left(2 \cdot \frac{V_{Ed}}{V_{pl,Rd}} - 1\right)^2 = \left(2 \cdot \frac{100}{400} - 1\right)^2 = 0.25",
            ),
        ],
    )
    def test_latex_output(self, representation: str, expected: str) -> None:
        """Test the latex implementation."""
        # Example values
        v_ed = 100  # kN
        v_pl_rd = 400  # kN

        form = Form5Dot10ReductionFactorShearArea(v_ed=v_ed, v_pl_rd=v_pl_rd).latex()

        actual = {
            "complete": form.complete,
            "short": form.short,
            "string": str(form),
        }

        assert actual[representation] == expected, f"{representation} representation failed."
