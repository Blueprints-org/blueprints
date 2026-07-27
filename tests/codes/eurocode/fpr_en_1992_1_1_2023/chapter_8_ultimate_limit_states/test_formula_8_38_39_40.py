"""Testing formulas 8.38, 8.39 and 8.40 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_38_39_40 import (
    Form8Dot38To40ReinforcementRatioPlanarMembers,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


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
            (100.0, -57.735, 0.012, 0.008, 30.0),  # v_ed_y is negative
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
            (-100.0, 57.735, 0.012, 0.008, 30.0),  # v_ed_x is negative
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
                r"\rho_l = \begin{cases} \rho_{l,x} & \text{if } \frac{v_{Ed,y}}{v_{Ed,x}} \leq 0.5 \\ "
                r"\rho_{l,x} \cdot \cos^4(\alpha_v) + \rho_{l,y} \cdot \sin^4(\alpha_v) "
                r"& \text{if } 0.5 < \frac{v_{Ed,y}}{v_{Ed,x}} < 2 \\ "
                r"\rho_{l,y} & \text{if } \frac{v_{Ed,y}}{v_{Ed,x}} \geq 2 \end{cases} = "
                r"\begin{cases} 0.012 & \text{if } \frac{57.735}{100.000} \leq 0.5 \\ "
                r"0.012 \cdot \cos^4(30.000) + 0.008 \cdot \sin^4(30.000) "
                r"& \text{if } 0.5 < \frac{57.735}{100.000} < 2 \\ "
                r"0.008 & \text{if } \frac{57.735}{100.000} \geq 2 \end{cases} = 0.007 \ -",
            ),
            (
                "complete_with_units",
                r"\rho_l = \begin{cases} \rho_{l,x} & \text{if } \frac{v_{Ed,y}}{v_{Ed,x}} \leq 0.5 \\ "
                r"\rho_{l,x} \cdot \cos^4(\alpha_v) + \rho_{l,y} \cdot \sin^4(\alpha_v) "
                r"& \text{if } 0.5 < \frac{v_{Ed,y}}{v_{Ed,x}} < 2 \\ "
                r"\rho_{l,y} & \text{if } \frac{v_{Ed,y}}{v_{Ed,x}} \geq 2 \end{cases} = "
                r"\begin{cases} 0.012 & \text{if } \frac{57.735 \ N/mm}{100.000 \ N/mm} \leq 0.5 \\ "
                r"0.012 \cdot \cos^4(30.000 \ degrees) + 0.008 \cdot \sin^4(30.000 \ degrees) "
                r"& \text{if } 0.5 < \frac{57.735 \ N/mm}{100.000 \ N/mm} < 2 \\ "
                r"0.008 & \text{if } \frac{57.735 \ N/mm}{100.000 \ N/mm} \geq 2 \end{cases} = 0.007 \ -",
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
