"""Testing formulas 8.22, 8.23 and 8.24 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_22_23_24 import Form8Dot22To24EffectiveDepth
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot22To24EffectiveDepth:
    """Validation for formulas 8.22, 8.23 and 8.24 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "expected"),
        [
            (100.0, 40.0, 300.0),  # ratio 0.4, formula 8.22
            (100.0, 50.0, 300.0),  # ratio 0.5 exactly, still formula 8.22
            (100.0, 100.0, 275.0),  # ratio 1.0, formula 8.23
            (100.0, 150.0, 275.0),  # ratio 1.5, formula 8.23
            (100.0, 200.0, 250.0),  # ratio 2.0 exactly, formula 8.24
            (100.0, 250.0, 250.0),  # ratio 2.5, formula 8.24
        ],
    )
    def test_evaluation(self, v_ed_x: float, v_ed_y: float, expected: float) -> None:
        """Tests the evaluation of the result for each of the three cases and both boundaries."""
        # Example values
        d_x = 300.0
        d_y = 250.0

        # Object to test
        formula = Form8Dot22To24EffectiveDepth(v_ed_x=v_ed_x, v_ed_y=v_ed_y, d_x=d_x, d_y=d_y)

        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y"),
        [
            (100.0, 150.0),  # both positive
            (100.0, -150.0),  # v_ed_y is negative
            (-100.0, 150.0),  # v_ed_x is negative
            (-100.0, -150.0),  # both negative
        ],
    )
    def test_sign_of_the_shear_forces_does_not_reach_the_result(self, v_ed_x: float, v_ed_y: float) -> None:
        """The ratio is taken on magnitudes, so all four sign combinations select the same branch.

        A signed ratio would turn negative as soon as one component does, and every negative value falls under
        Formula (8.22) regardless of which direction actually carries the shear. Formula (8.21) reaches the same
        place by squaring both components.
        """
        formula = Form8Dot22To24EffectiveDepth(v_ed_x=v_ed_x, v_ed_y=v_ed_y, d_x=300.0, d_y=250.0)

        # ratio 1.5, so the middle branch of Formula (8.23)
        assert formula == pytest.approx(expected=275.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "d_x", "d_y"),
        [
            (0.0, 100.0, 300.0, 250.0),  # v_ed_x is zero, for which the ratio is undefined
            (100.0, 100.0, 0.0, 250.0),  # d_x is zero, which is not a cross-section
            (100.0, 100.0, -300.0, 250.0),  # d_x is negative
            (100.0, 100.0, 300.0, 0.0),  # d_y is zero
            (100.0, 100.0, 300.0, -250.0),  # d_y is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, v_ed_x: float, v_ed_y: float, d_x: float, d_y: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less.

        The guard on the shear force is on its magnitude, so a negative one passes it and only zero is refused.
        """
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot22To24EffectiveDepth(v_ed_x=v_ed_x, v_ed_y=v_ed_y, d_x=d_x, d_y=d_y)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"d = \begin{cases} d_x & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \leq 0.5 \\ "
                    r"0.5 \cdot (d_x + d_y) & \text{if } 0.5 < \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} < 2 \\ "
                    r"d_y & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \geq 2 \end{cases} = "
                    r"\begin{cases} 300.000 & \text{if } \frac{\left|100.000\right|}{\left|100.000\right|} \leq 0.5 \\ "
                    r"0.5 \cdot (300.000 + 250.000) & \text{if } 0.5 < \frac{\left|100.000\right|}{\left|100.000\right|} < 2 \\ "
                    r"250.000 & \text{if } \frac{\left|100.000\right|}{\left|100.000\right|} \geq 2 \end{cases} = "
                    r"0.5 \cdot (300.000 + 250.000) = 275.000 \ mm"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"d = \begin{cases} d_x & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \leq 0.5 \\ "
                    r"0.5 \cdot (d_x + d_y) & \text{if } 0.5 < \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} < 2 \\ "
                    r"d_y & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \geq 2 \end{cases} = "
                    r"\begin{cases} 300.000 \ mm & \text{if } \frac{\left|100.000 \ N/mm\right|}{\left|100.000 \ N/mm\right|} \leq 0.5 \\ "
                    r"0.5 \cdot (300.000 \ mm + 250.000 \ mm) & "
                    r"\text{if } 0.5 < \frac{\left|100.000 \ N/mm\right|}{\left|100.000 \ N/mm\right|} < 2 \\ "
                    r"250.000 \ mm & \text{if } \frac{\left|100.000 \ N/mm\right|}{\left|100.000 \ N/mm\right|} \geq 2 \end{cases} = "
                    r"0.5 \cdot (300.000 + 250.000) = 275.000 \ mm"
                ),
            ),
            ("short", r"d = 275.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_x = 100.0
        v_ed_y = 100.0
        d_x = 300.0
        d_y = 250.0

        # Object to test
        latex = Form8Dot22To24EffectiveDepth(v_ed_x=v_ed_x, v_ed_y=v_ed_y, d_x=d_x, d_y=d_y).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."

    def test_no_intermediate_result_outside_the_middle_branch(self) -> None:
        """Only Formula (8.23) has a step between the selected expression and the result."""
        outer = Form8Dot22To24EffectiveDepth(v_ed_x=100.0, v_ed_y=40.0, d_x=300.0, d_y=250.0).latex()
        middle = Form8Dot22To24EffectiveDepth(v_ed_x=100.0, v_ed_y=100.0, d_x=300.0, d_y=250.0).latex()

        assert outer.intermediate_result == ""
        assert middle.intermediate_result == r"0.5 \cdot (300.000 + 250.000)"
