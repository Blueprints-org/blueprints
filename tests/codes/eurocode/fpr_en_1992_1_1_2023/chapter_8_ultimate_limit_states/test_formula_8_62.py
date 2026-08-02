"""Testing formula 8.62 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_62 import (
    Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot62EnhancedShearStressResistanceInclinedShearReinforcement:
    """Validation for formula 8.62 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("rho_w", "expected"),
        [
            # 0.5 * 20 * (2 - 1) / (1 + 2^2) + 0.002 * 435 * (1 + cot(60)) * sin(60) = 2.0 + 1.188442,
            # below the limit of 0.5 * 20 * (2 + cot(60)) / (1 + 2^2) = 5.154701
            (0.002, 3.1884421012924618),
            # at five times the reinforcement ratio the sum reaches 7.942211, so the limit governs
            (0.01, 5.154700538379252),
        ],
    )
    def test_evaluation(self, rho_w: float, expected: float) -> None:
        """Tests the evaluation of the result, both below and at the upper bound."""
        # Create object to test
        formula = Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
            nu=0.5,
            f_cd=20.0,
            cot_theta=2.0,
            cot_beta_incl=1.0,
            rho_w=rho_w,
            f_ywd=435.0,
            alpha_w=60.0,
        )

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_no_clamp_outside_the_condition_of_application(self) -> None:
        """The enhancement applies where the load sits closer to the support than z * cot(theta), which means
        cot(beta_incl) < cot(theta). That is a condition of application and not a bound, so a larger
        cot(beta_incl) makes the first term negative and the formula returns that result unchanged.
        """
        # Example values, with cot_beta_incl deliberately larger than cot_theta
        formula = Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
            nu=0.5,
            f_cd=20.0,
            cot_theta=2.0,
            cot_beta_incl=3.0,
            rho_w=0.002,
            f_ywd=435.0,
            alpha_w=60.0,
        )

        # 0.5 * 20 * (2 - 3) / 5 + 0.002 * 435 * (3 + cot(60)) * sin(60) = -2.0 + 0.87 * 3.098076
        assert formula == pytest.approx(expected=0.6953263038773846, rel=1e-4)

    @pytest.mark.parametrize(
        ("nu", "f_cd", "cot_theta", "cot_beta_incl", "rho_w", "f_ywd"),
        [
            (-0.5, 20.0, 2.0, 1.0, 0.002, 435.0),  # nu is negative
            (0.5, -20.0, 2.0, 1.0, 0.002, 435.0),  # f_cd is negative
            (0.5, 20.0, -2.0, 1.0, 0.002, 435.0),  # cot_theta is negative
            (0.5, 20.0, 2.0, -1.0, 0.002, 435.0),  # cot_beta_incl is negative
            (0.5, 20.0, 2.0, 1.0, -0.002, 435.0),  # rho_w is negative
            (0.5, 20.0, 2.0, 1.0, 0.002, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(
        self, nu: float, f_cd: float, cot_theta: float, cot_beta_incl: float, rho_w: float, f_ywd: float
    ) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
                nu=nu,
                f_cd=f_cd,
                cot_theta=cot_theta,
                cot_beta_incl=cot_beta_incl,
                rho_w=rho_w,
                f_ywd=f_ywd,
                alpha_w=60.0,
            )

    @pytest.mark.parametrize("alpha_w", [-60.0, 0.0])
    def test_raise_error_when_less_or_equal_to_zero(self, alpha_w: float) -> None:
        """Test if error is raised for an inclination that is not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
                nu=0.5,
                f_cd=20.0,
                cot_theta=2.0,
                cot_beta_incl=1.0,
                rho_w=0.002,
                f_ywd=435.0,
                alpha_w=alpha_w,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rd} = \min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
                r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot "
                r"\left(\cot(\beta_{incl}) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w), "
                r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta) + \cot(\alpha_w)}{1 + \left(\cot(\theta)\right)^2}\right) = "
                r"\min\left(0.500 \cdot 20.000 \cdot \frac{2.000 - 1.000}"
                r"{1 + \left(2.000\right)^2} + 0.002 \cdot 435.000 \cdot "
                r"\left(1.000 + \cot(60.000)\right) \cdot \sin(60.000), "
                r"0.500 \cdot 20.000 \cdot \frac{2.000 + \cot(60.000)}{1 + \left(2.000\right)^2}\right) = 3.188 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rd} = \min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
                r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot "
                r"\left(\cot(\beta_{incl}) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w), "
                r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta) + \cot(\alpha_w)}{1 + \left(\cot(\theta)\right)^2}\right) = "
                r"\min\left(0.500 \cdot 20.000 \ MPa \cdot \frac{2.000 - 1.000}"
                r"{1 + \left(2.000\right)^2} + 0.002 \cdot 435.000 \ MPa \cdot "
                r"\left(1.000 + \cot(60.000 \ degrees)\right) \cdot \sin(60.000 \ degrees), "
                r"0.500 \cdot 20.000 \ MPa \cdot \frac{2.000 + \cot(60.000 \ degrees)}"
                r"{1 + \left(2.000\right)^2}\right) = 3.188 \ MPa",
            ),
            ("short", r"\tau_{Rd} = 3.188 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
            nu=0.5,
            f_cd=20.0,
            cot_theta=2.0,
            cot_beta_incl=1.0,
            rho_w=0.002,
            f_ywd=435.0,
            alpha_w=60.0,
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
