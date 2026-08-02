"""Testing formula 8.63 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_63 import (
    Form8Dot63StressInInclinedShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot63StressInInclinedShearReinforcement:
    """Validation for formula 8.63 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "expected"),
        [
            # 200000 * ((0.001 + 0.001) * (0.5 + cot(60))^2 / (1 + cot(60)^2) - 0.001), well below f_ywd.
            # This is the shallow inclination the formula exists for: cot_theta = 0.5 < tan(30) = 0.577.
            (0.5, 148.2050807568878),
            # at cot_theta = 2.0 the expression reaches 1792.820, so f_ywd governs
            (2.0, 435.0),
        ],
    )
    def test_evaluation(self, cot_theta: float, expected: float) -> None:
        """Tests the evaluation of the result, both below and at the upper bound."""
        # Create object to test
        formula = Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.001, cot_theta=cot_theta, alpha_w=60.0, f_ywd=435.0)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """The standard prints only an upper bound. A small cotangent combined with a small longitudinal strain
        gives a negative stress, and that result is returned unchanged rather than clamped, since a clamp would
        be an addition beyond the printed text.
        """
        # Example values
        formula = Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.0, cot_theta=0.0, alpha_w=60.0, f_ywd=435.0)

        # 200000 * (0.001 * cot(60)^2 / (1 + cot(60)^2) - 0.001) = 200000 * (0.00025 - 0.001)
        assert formula == pytest.approx(expected=-150.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("e_s", "epsilon_x", "cot_theta", "f_ywd"),
        [
            (-200000.0, 0.001, 0.5, 435.0),  # e_s is negative
            (200000.0, -0.001, 0.5, 435.0),  # epsilon_x is negative
            (200000.0, 0.001, -0.5, 435.0),  # cot_theta is negative
            (200000.0, 0.001, 0.5, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, e_s: float, epsilon_x: float, cot_theta: float, f_ywd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot63StressInInclinedShearReinforcement(e_s=e_s, epsilon_x=epsilon_x, cot_theta=cot_theta, alpha_w=60.0, f_ywd=f_ywd)

    @pytest.mark.parametrize("alpha_w", [-60.0, 0.0])
    def test_raise_error_when_less_or_equal_to_zero(self, alpha_w: float) -> None:
        """Test if error is raised for an inclination that is not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.001, cot_theta=0.5, alpha_w=alpha_w, f_ywd=435.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\sigma_{swd} = \min\left(E_s \cdot \left[\left(\varepsilon_x + 0.001\right) \cdot "
                r"\frac{\left(\cot(\theta) + \cot(\alpha_w)\right)^2}{1 + \left(\cot(\alpha_w)\right)^2} "
                r"- 0.001\right], f_{ywd}\right) = "
                r"\min\left(200000.000 \cdot \left[\left(0.001 + 0.001\right) \cdot "
                r"\frac{\left(0.500 + \cot(60.000)\right)^2}{1 + \left(\cot(60.000)\right)^2} "
                r"- 0.001\right], 435.000\right) = 148.205 \ MPa",
            ),
            (
                "complete_with_units",
                r"\sigma_{swd} = \min\left(E_s \cdot \left[\left(\varepsilon_x + 0.001\right) \cdot "
                r"\frac{\left(\cot(\theta) + \cot(\alpha_w)\right)^2}{1 + \left(\cot(\alpha_w)\right)^2} "
                r"- 0.001\right], f_{ywd}\right) = "
                r"\min\left(200000.000 \ MPa \cdot \left[\left(0.001 + 0.001\right) \cdot "
                r"\frac{\left(0.500 + \cot(60.000 \ degrees)\right)^2}{1 + \left(\cot(60.000 \ degrees)\right)^2} "
                r"- 0.001\right], 435.000 \ MPa\right) = 148.205 \ MPa",
            ),
            ("short", r"\sigma_{swd} = 148.205 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.001, cot_theta=0.5, alpha_w=60.0, f_ywd=435.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
