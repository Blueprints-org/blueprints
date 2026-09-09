"""Testing formula 8.62 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_62 import (
    Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement,
)
from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_63 import (
    Form8Dot63StressInInclinedShearReinforcement,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angles chosen so that their cotangents are round numbers, which keeps the hand calculations readable
THETA_COT_0_2 = 78.69006752598  # cot(theta) = 0.2
THETA_COT_2 = 26.565051177078  # cot(theta) = 2
BETA_COT_1 = 45.0  # cot(beta_incl) = 1
BETA_COT_3 = 18.434948822922  # cot(beta_incl) = 3


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
            theta=THETA_COT_2,
            beta_incl=BETA_COT_1,
            rho_w=rho_w,
            f_ywd=435.0,
            alpha_w=60.0,
        )

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_no_clamp_outside_the_condition_of_application(self) -> None:
        """The enhancement applies where the load sits closer to the support than z * cot(theta), which means
        beta_incl > theta. That is a condition of application and not a bound, so a flatter beta_incl makes the
        first term negative and the formula returns that result unchanged.
        """
        # Example values, with beta_incl deliberately flatter than theta
        formula = Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
            nu=0.5,
            f_cd=20.0,
            theta=THETA_COT_2,
            beta_incl=BETA_COT_3,
            rho_w=0.002,
            f_ywd=435.0,
            alpha_w=60.0,
        )

        # 0.5 * 20 * (2 - 3) / 5 + 0.002 * 435 * (3 + cot(60)) * sin(60) = -2.0 + 0.87 * 3.098076
        assert formula == pytest.approx(expected=0.6953263038773846, rel=1e-4)

    def test_accepts_the_negative_stress_of_formula_8_63(self) -> None:
        r"""For [$\cot\theta < \tan(\alpha_w/2)$] the standard requires f_ywd to be replaced by the stress of
        Formula (8.63), which carries no printed lower bound and is negative over much of its range. Guarding
        this argument against negative values would block the substitution the standard prescribes, so it is
        not guarded.
        """
        # cot(theta) = 0.2 lies below tan(30) = 0.577, which is the case (8.63) exists for
        sigma_swd = Form8Dot63StressInInclinedShearReinforcement(e_s=200000.0, epsilon_x=0.0, theta=THETA_COT_0_2, alpha_w=60.0, f_ywd=435.0)
        assert sigma_swd == pytest.approx(expected=-109.3589838486233, rel=1e-4)

        formula = Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
            nu=0.5,
            f_cd=20.0,
            theta=THETA_COT_0_2,
            beta_incl=BETA_COT_1,
            rho_w=0.002,
            f_ywd=sigma_swd,
            alpha_w=60.0,
        )

        # 0.5 * 20 * (0.2 - 1) / (1 + 0.2^2) + 0.002 * -109.358984 * (1 + cot(60)) * sin(60) = -7.692308 - 0.298795
        assert formula == pytest.approx(expected=-7.991102630182123, rel=1e-4)

    @pytest.mark.parametrize(
        ("nu", "f_cd", "rho_w"),
        [
            (-0.5, 20.0, 0.002),  # nu is negative
            (0.5, -20.0, 0.002),  # f_cd is negative
            (0.5, 20.0, -0.002),  # rho_w is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, nu: float, f_cd: float, rho_w: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
                nu=nu,
                f_cd=f_cd,
                theta=THETA_COT_2,
                beta_incl=BETA_COT_1,
                rho_w=rho_w,
                f_ywd=435.0,
                alpha_w=60.0,
            )

    @pytest.mark.parametrize(
        ("theta", "beta_incl", "alpha_w"),
        [
            (-THETA_COT_2, BETA_COT_1, 60.0),  # theta is negative
            (0.0, BETA_COT_1, 60.0),  # theta is zero, for which the cotangent diverges
            (THETA_COT_2, -BETA_COT_1, 60.0),  # beta_incl is negative
            (THETA_COT_2, 0.0, 60.0),  # beta_incl is zero, for which the cotangent diverges
            (THETA_COT_2, BETA_COT_1, -60.0),  # alpha_w is negative
            (THETA_COT_2, BETA_COT_1, 0.0),  # alpha_w is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_the_angles_are_less_or_equal_to_zero(self, theta: float, beta_incl: float, alpha_w: float) -> None:
        """Test if error is raised for angles that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
                nu=0.5,
                f_cd=20.0,
                theta=theta,
                beta_incl=beta_incl,
                rho_w=0.002,
                f_ywd=435.0,
                alpha_w=alpha_w,
            )

    @pytest.mark.parametrize(
        ("theta", "beta_incl", "alpha_w"),
        [
            (120.0, BETA_COT_1, 60.0),  # theta exceeds 90 degrees
            (THETA_COT_2, 120.0, 60.0),  # beta_incl exceeds 90 degrees
            (THETA_COT_2, BETA_COT_1, 120.0),  # alpha_w exceeds 90 degrees
        ],
    )
    def test_raise_error_when_the_angles_exceed_90_degrees(self, theta: float, beta_incl: float, alpha_w: float) -> None:
        """All three angles are inclinations to the member axis, so none of them can pass 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(
                nu=0.5,
                f_cd=20.0,
                theta=theta,
                beta_incl=beta_incl,
                rho_w=0.002,
                f_ywd=435.0,
                alpha_w=alpha_w,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rd} = \min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
                    r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot "
                    r"\left(\cot(\beta_{incl}) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w), "
                    r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta) + \cot(\alpha_w)}{1 + \left(\cot(\theta)\right)^2}\right) = "
                    r"\min\left(0.500 \cdot 20.000 \cdot \frac{\cot(26.565) - \cot(45.000)}"
                    r"{1 + \left(\cot(26.565)\right)^2} + 0.002 \cdot 435.000 \cdot "
                    r"\left(\cot(45.000) + \cot(60.000)\right) \cdot \sin(60.000), "
                    r"0.500 \cdot 20.000 \cdot \frac{\cot(26.565) + \cot(60.000)}"
                    r"{1 + \left(\cot(26.565)\right)^2}\right) = 3.188 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rd} = \min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
                    r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot "
                    r"\left(\cot(\beta_{incl}) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w), "
                    r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta) + \cot(\alpha_w)}{1 + \left(\cot(\theta)\right)^2}\right) = "
                    r"\min\left(0.500 \cdot 20.000 \ MPa \cdot \frac{\cot(26.565 ^\circ) - \cot(45.000 ^\circ)}"
                    r"{1 + \left(\cot(26.565 ^\circ)\right)^2} + 0.002 \cdot 435.000 \ MPa \cdot "
                    r"\left(\cot(45.000 ^\circ) + \cot(60.000 ^\circ)\right) \cdot \sin(60.000 ^\circ), "
                    r"0.500 \cdot 20.000 \ MPa \cdot \frac{\cot(26.565 ^\circ) + \cot(60.000 ^\circ)}"
                    r"{1 + \left(\cot(26.565 ^\circ)\right)^2}\right) = 3.188 \ MPa"
                ),
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
            theta=THETA_COT_2,
            beta_incl=BETA_COT_1,
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
