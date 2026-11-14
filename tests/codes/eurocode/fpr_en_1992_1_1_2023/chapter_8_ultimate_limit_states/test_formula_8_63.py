"""Testing formula 8.63 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_63 import (
    Form8Dot63StressInInclinedShearReinforcement,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angles chosen so that their cotangents are round numbers, which keeps the hand calculations readable
THETA_COT_0_2 = 78.69006752598  # cot(theta) = 0.2
THETA_COT_0_5 = 63.434948822922  # cot(theta) = 0.5
THETA_COT_2 = 26.565051177078  # cot(theta) = 2


class TestForm8Dot63StressInInclinedShearReinforcement:
    """Validation for formula 8.63 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("theta", "expected"),
        [
            # 200000 * ((0.001 + 0.001) * (0.5 + cot(60))^2 / (1 + cot(60)^2) - 0.001), well below f_ywd.
            # This is the shallow inclination the formula exists for: cot(theta) = 0.5 < tan(30) = 0.577.
            (THETA_COT_0_5, 148.2050807568878),
            # at cot(theta) = 2.0 the expression reaches 1792.820, so f_ywd governs
            (THETA_COT_2, 435.0),
        ],
    )
    def test_evaluation(self, theta: float, expected: float) -> None:
        """Tests the evaluation of the result, both below and at the upper bound."""
        # Create object to test
        formula = Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.001, theta=theta, alpha_w=60.0, f_ywd=435.0)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """The standard prints only an upper bound. A shallow compression field combined with a small
        longitudinal strain gives a negative stress, and that result is returned unchanged rather than clamped,
        since a clamp would be an addition beyond the printed text.
        """
        # Example values, with cot(theta) = 0.2 well inside the range this formula exists for
        formula = Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.0, theta=THETA_COT_0_2, alpha_w=60.0, f_ywd=435.0)

        # 200000 * (0.001 * (0.2 + cot(60))^2 / (1 + cot(60)^2) - 0.001) = 200000 * -0.000546795
        assert formula == pytest.approx(expected=-109.3589838486233, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_s", "epsilon_x", "f_ywd"),
        [
            (-200000.0, 0.001, 435.0),  # e_s is negative
            (200000.0, -0.001, 435.0),  # epsilon_x is negative
            (200000.0, 0.001, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, e_s: float, epsilon_x: float, f_ywd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot63StressInInclinedShearReinforcement(e_s=e_s, epsilon_x=epsilon_x, theta=THETA_COT_0_5, alpha_w=60.0, f_ywd=f_ywd)

    @pytest.mark.parametrize(
        ("theta", "alpha_w"),
        [
            (-THETA_COT_0_5, 60.0),  # theta is negative
            (0.0, 60.0),  # theta is zero, for which the cotangent diverges
            (THETA_COT_0_5, -60.0),  # alpha_w is negative
            (THETA_COT_0_5, 0.0),  # alpha_w is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_the_angles_are_less_or_equal_to_zero(self, theta: float, alpha_w: float) -> None:
        """Test if error is raised for angles that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.001, theta=theta, alpha_w=alpha_w, f_ywd=435.0)

    @pytest.mark.parametrize(
        ("theta", "alpha_w"),
        [
            (120.0, 60.0),  # theta exceeds 90 degrees
            (THETA_COT_0_5, 120.0),  # alpha_w exceeds 90 degrees, which the standard says should be avoided
        ],
    )
    def test_raise_error_when_the_angles_exceed_90_degrees(self, theta: float, alpha_w: float) -> None:
        """Both angles are inclinations to the member axis, so neither can pass 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.001, theta=theta, alpha_w=alpha_w, f_ywd=435.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\sigma_{swd} = \min\left(E_s \cdot \left[\left(\varepsilon_x + 0.001\right) \cdot "
                    r"\frac{\left(\cot(\theta) + \cot(\alpha_w)\right)^2}{1 + \left(\cot(\alpha_w)\right)^2} "
                    r"- 0.001\right], f_{ywd}\right) = "
                    r"\min\left(200000.000 \cdot \left[\left(0.001 + 0.001\right) \cdot "
                    r"\frac{\left(\cot(63.435) + \cot(60.000)\right)^2}{1 + \left(\cot(60.000)\right)^2} "
                    r"- 0.001\right], 435.000\right) = 148.205 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\sigma_{swd} = \min\left(E_s \cdot \left[\left(\varepsilon_x + 0.001\right) \cdot "
                    r"\frac{\left(\cot(\theta) + \cot(\alpha_w)\right)^2}{1 + \left(\cot(\alpha_w)\right)^2} "
                    r"- 0.001\right], f_{ywd}\right) = "
                    r"\min\left(200000.000 \ MPa \cdot \left[\left(0.001 + 0.001\right) \cdot "
                    r"\frac{\left(\cot(63.435 ^\circ) + \cot(60.000 ^\circ)\right)^2}{1 + \left(\cot(60.000 ^\circ)\right)^2} "
                    r"- 0.001\right], 435.000 \ MPa\right) = 148.205 \ MPa"
                ),
            ),
            ("short", r"\sigma_{swd} = 148.205 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot63StressInInclinedShearReinforcement(
            e_s=200000.0, epsilon_x=0.001, theta=THETA_COT_0_5, alpha_w=60.0, f_ywd=435.0
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
