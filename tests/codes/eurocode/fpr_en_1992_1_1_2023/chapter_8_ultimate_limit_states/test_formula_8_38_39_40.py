"""Testing formulas 8.38, 8.39 and 8.40 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_38_39_40 import (
    Form8Dot38To40ReinforcementRatioPlanarMembers,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot38To40ReinforcementRatioPlanarMembers:
    """Validation for formulas 8.38, 8.39 and 8.40 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "alpha_v", "expected"),
        [
            # Formula (8.38), ratio 0.4 <= 0.5, so rho_l = rho_l_x
            (100.0, 40.0, 21.801, 0.012),
            # Formula (8.38) at the boundary, ratio exactly 0.5
            (100.0, 50.0, 26.565, 0.012),
            # Formula (8.39), ratio 0.57735 = tan(30 degrees), so rho_l = 0.012 * 0.5625 + 0.008 * 0.0625
            (100.0, 57.735, 30.0, 0.00725),
            # Formula (8.39), ratio 1.0 = tan(45 degrees), so rho_l = 0.012 * 0.25 + 0.008 * 0.25
            (100.0, 100.0, 45.0, 0.005),
            # Formula (8.40) at the boundary, ratio exactly 2
            (100.0, 200.0, 63.435, 0.008),
            # Formula (8.40), ratio 2.5 >= 2, so rho_l = rho_l_y
            (100.0, 250.0, 68.199, 0.008),
        ],
    )
    def test_evaluation(self, v_ed_x: float, v_ed_y: float, alpha_v: float, expected: float) -> None:
        """Tests the evaluation of the result for each of the three branches."""
        # Example values
        rho_l_x = 0.012
        rho_l_y = 0.008

        # Create object to test
        formula = Form8Dot38To40ReinforcementRatioPlanarMembers(
            v_ed_x=v_ed_x,
            v_ed_y=v_ed_y,
            rho_l_x=rho_l_x,
            rho_l_y=rho_l_y,
            alpha_v=alpha_v,
        )

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "rho_l_x", "rho_l_y", "alpha_v"),
        [
            (100.0, 57.735, -0.012, 0.008, 30.0),  # rho_l_x is negative
            (100.0, 57.735, 0.012, -0.008, 30.0),  # rho_l_y is negative
            (100.0, 57.735, 0.012, 0.008, -30.0),  # alpha_v is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, v_ed_x: float, v_ed_y: float, rho_l_x: float, rho_l_y: float, alpha_v: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot38To40ReinforcementRatioPlanarMembers(
                v_ed_x=v_ed_x,
                v_ed_y=v_ed_y,
                rho_l_x=rho_l_x,
                rho_l_y=rho_l_y,
                alpha_v=alpha_v,
            )

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "rho_l_x", "rho_l_y", "alpha_v"),
        [
            (0.0, 57.735, 0.012, 0.008, 30.0),  # v_ed_x is zero, the ratio is undefined
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, v_ed_x: float, v_ed_y: float, rho_l_x: float, rho_l_y: float, alpha_v: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot38To40ReinforcementRatioPlanarMembers(
                v_ed_x=v_ed_x,
                v_ed_y=v_ed_y,
                rho_l_x=rho_l_x,
                rho_l_y=rho_l_y,
                alpha_v=alpha_v,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho_l = \begin{cases} \rho_{l,x} & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \leq 0.5 \\ "
                r"\rho_{l,x} \cdot \cos^4(\alpha_v) + \rho_{l,y} \cdot \sin^4(\alpha_v) "
                r"& \text{if } 0.5 < \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} < 2 \\ "
                r"\rho_{l,y} & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \geq 2 \end{cases} = "
                r"\begin{cases} 0.012 & \text{if } \frac{\left|57.735\right|}{\left|100.000\right|} \leq 0.5 \\ "
                r"0.012 \cdot \cos^4(30.000) + 0.008 \cdot \sin^4(30.000) "
                r"& \text{if } 0.5 < \frac{\left|57.735\right|}{\left|100.000\right|} < 2 \\ "
                r"0.008 & \text{if } \frac{\left|57.735\right|}{\left|100.000\right|} \geq 2 \end{cases} = 0.007 \ -",
            ),
            (
                "complete_with_units",
                r"\rho_l = \begin{cases} \rho_{l,x} & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \leq 0.5 \\ "
                r"\rho_{l,x} \cdot \cos^4(\alpha_v) + \rho_{l,y} \cdot \sin^4(\alpha_v) "
                r"& \text{if } 0.5 < \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} < 2 \\ "
                r"\rho_{l,y} & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \geq 2 \end{cases} = "
                r"\begin{cases} 0.012 & \text{if } \frac{\left|57.735 \ N/mm\right|}{\left|100.000 \ N/mm\right|} \leq 0.5 \\ "
                r"0.012 \cdot \cos^4(30.000 \ degrees) + 0.008 \cdot \sin^4(30.000 \ degrees) "
                r"& \text{if } 0.5 < \frac{\left|57.735 \ N/mm\right|}{\left|100.000 \ N/mm\right|} < 2 \\ "
                r"0.008 & \text{if } \frac{\left|57.735 \ N/mm\right|}{\left|100.000 \ N/mm\right|} \geq 2 \end{cases} = 0.007 \ -",
            ),
            ("short", r"\rho_l = 0.007 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_x = 100.0
        v_ed_y = 57.735
        rho_l_x = 0.012
        rho_l_y = 0.008
        alpha_v = 30.0

        # Object to test
        test_latex = Form8Dot38To40ReinforcementRatioPlanarMembers(
            v_ed_x=v_ed_x,
            v_ed_y=v_ed_y,
            rho_l_x=rho_l_x,
            rho_l_y=rho_l_y,
            alpha_v=alpha_v,
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y"),
        [
            (100.0, 57.735),  # both positive
            (100.0, -57.735),  # v_ed_y is negative
            (-100.0, 57.735),  # v_ed_x is negative
            (-100.0, -57.735),  # both negative
        ],
    )
    def test_sign_of_the_shear_forces_does_not_reach_the_result(self, v_ed_x: float, v_ed_y: float) -> None:
        """The ratio is taken on magnitudes, so all four sign combinations select the same branch.

        This matches Formulas (8.22) to (8.24), which the standard writes with the same ratio and the same
        two boundaries.
        """
        formula = Form8Dot38To40ReinforcementRatioPlanarMembers(v_ed_x=v_ed_x, v_ed_y=v_ed_y, rho_l_x=0.012, rho_l_y=0.008, alpha_v=30.0)

        assert formula == pytest.approx(expected=0.00725, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_x", "v_ed_y", "expected_alpha_v", "expected"),
        [
            (100.0, 57.735, 30.0, 0.00725),  # Formula (8.39), the branch that uses the angle
            (100.0, 40.0, 21.801409, 0.012),  # Formula (8.38)
            (100.0, 250.0, 68.198591, 0.008),  # Formula (8.40)
            (-100.0, -57.735, 30.0, 0.00725),  # the magnitudes decide the angle as well
        ],
    )
    def test_angle_defaults_to_formula_8_26(self, v_ed_x: float, v_ed_y: float, expected_alpha_v: float, expected: float) -> None:
        """Leaving out the angle computes it from the two shear forces, as 8.2.1(5) defines it."""
        formula = Form8Dot38To40ReinforcementRatioPlanarMembers(v_ed_x=v_ed_x, v_ed_y=v_ed_y, rho_l_x=0.012, rho_l_y=0.008)

        assert formula.alpha_v == pytest.approx(expected=expected_alpha_v, rel=1e-6)
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_raise_error_when_the_angle_exceeds_90_degrees(self) -> None:
        """Formula (8.26) is an arctangent of two magnitudes, so it can never exceed 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot38To40ReinforcementRatioPlanarMembers(v_ed_x=100.0, v_ed_y=57.735, rho_l_x=0.012, rho_l_y=0.008, alpha_v=120.0)
