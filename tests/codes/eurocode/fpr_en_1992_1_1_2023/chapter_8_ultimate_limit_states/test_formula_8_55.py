"""Testing formula 8.55 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_55 import Form8Dot55EnhancedShearStressResistance
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angles chosen so that their cotangents are round numbers, which keeps the hand calculations readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2
BETA_COT_1 = 45.0  # cot(beta_incl) = 1
BETA_COT_3 = 18.434948822922  # cot(beta_incl) = 3


class TestForm8Dot55EnhancedShearStressResistance:
    """Validation for formula 8.55 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("rho_w", "expected"),
        [
            # 0.5 * 20 * (2 - 1) / (1 + 2^2) + 0.002 * 435 * 1 = 2.0 + 0.87, below the limit of 4.0
            (0.002, 2.87),
            # 2.0 + 0.01 * 435 * 1 = 6.35, so the upper bound 0.5 * 20 * 2 / (1 + 2^2) = 4.0 governs
            (0.01, 4.0),
        ],
    )
    def test_evaluation(self, rho_w: float, expected: float) -> None:
        """Tests the evaluation of the result, both below and at the upper bound."""
        # Example values
        formula = Form8Dot55EnhancedShearStressResistance(
            nu=0.5,
            f_cd=20.0,
            theta=THETA_COT_2,
            beta_incl=BETA_COT_1,
            rho_w=rho_w,
            f_ywd=435.0,
        )

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_no_clamp_outside_the_condition_of_application(self) -> None:
        """The enhancement applies where the load sits closer to the support than z * cot(theta), which means
        beta_incl > theta. That is a condition of application and not a bound, so a flatter beta_incl makes the
        first term negative and the formula returns that result unchanged.
        """
        # Example values, with beta_incl deliberately flatter than theta
        formula = Form8Dot55EnhancedShearStressResistance(
            nu=0.5,
            f_cd=20.0,
            theta=THETA_COT_2,
            beta_incl=BETA_COT_3,
            rho_w=0.002,
            f_ywd=435.0,
        )

        # 0.5 * 20 * (2 - 3) / (1 + 2^2) + 0.002 * 435 * 3 = -2.0 + 2.61
        assert formula == pytest.approx(expected=0.61, rel=1e-4)

    @pytest.mark.parametrize(
        ("nu", "f_cd", "rho_w", "f_ywd"),
        [
            (-0.5, 20.0, 0.002, 435.0),  # nu is negative
            (0.5, -20.0, 0.002, 435.0),  # f_cd is negative
            (0.5, 20.0, -0.002, 435.0),  # rho_w is negative
            (0.5, 20.0, 0.002, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, nu: float, f_cd: float, rho_w: float, f_ywd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot55EnhancedShearStressResistance(
                nu=nu,
                f_cd=f_cd,
                theta=THETA_COT_2,
                beta_incl=BETA_COT_1,
                rho_w=rho_w,
                f_ywd=f_ywd,
            )

    @pytest.mark.parametrize(
        ("theta", "beta_incl"),
        [
            (-THETA_COT_2, BETA_COT_1),  # theta is negative
            (0.0, BETA_COT_1),  # theta is zero, for which the cotangent diverges
            (THETA_COT_2, -BETA_COT_1),  # beta_incl is negative
            (THETA_COT_2, 0.0),  # beta_incl is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_the_angles_are_less_or_equal_to_zero(self, theta: float, beta_incl: float) -> None:
        """Test if error is raised for angles that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot55EnhancedShearStressResistance(
                nu=0.5,
                f_cd=20.0,
                theta=theta,
                beta_incl=beta_incl,
                rho_w=0.002,
                f_ywd=435.0,
            )

    @pytest.mark.parametrize(
        ("theta", "beta_incl"),
        [
            (120.0, BETA_COT_1),  # theta exceeds 90 degrees
            (THETA_COT_2, 120.0),  # beta_incl exceeds 90 degrees
        ],
    )
    def test_raise_error_when_the_angles_exceed_90_degrees(self, theta: float, beta_incl: float) -> None:
        """Both angles are inclinations to the member axis, so neither can pass 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot55EnhancedShearStressResistance(
                nu=0.5,
                f_cd=20.0,
                theta=theta,
                beta_incl=beta_incl,
                rho_w=0.002,
                f_ywd=435.0,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rd} = \min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
                r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot \cot(\beta_{incl}), "
                r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta)}{1 + \left(\cot(\theta)\right)^2}\right) = "
                r"\min\left(0.500 \cdot 20.000 \cdot \frac{\cot(26.565) - \cot(45.000)}"
                r"{1 + \left(\cot(26.565)\right)^2} + 0.002 \cdot 435.000 \cdot \cot(45.000), "
                r"0.500 \cdot 20.000 \cdot \frac{\cot(26.565)}{1 + \left(\cot(26.565)\right)^2}\right) = 2.870 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rd} = \min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
                r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot \cot(\beta_{incl}), "
                r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta)}{1 + \left(\cot(\theta)\right)^2}\right) = "
                r"\min\left(0.500 \cdot 20.000 \ MPa \cdot \frac{\cot(26.565 ^\circ) - \cot(45.000 ^\circ)}"
                r"{1 + \left(\cot(26.565 ^\circ)\right)^2} + 0.002 \cdot 435.000 \ MPa \cdot \cot(45.000 ^\circ), "
                r"0.500 \cdot 20.000 \ MPa \cdot \frac{\cot(26.565 ^\circ)}{1 + \left(\cot(26.565 ^\circ)\right)^2}\right) = 2.870 \ MPa",
            ),
            ("short", r"\tau_{Rd} = 2.870 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot55EnhancedShearStressResistance(
            nu=0.5,
            f_cd=20.0,
            theta=THETA_COT_2,
            beta_incl=BETA_COT_1,
            rho_w=0.002,
            f_ywd=435.0,
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
