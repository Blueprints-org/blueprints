"""Testing formula 8.60 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_60 import (
    Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angle chosen so that its cotangent is a round number, which keeps the hand calculations readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2


class TestForm8Dot60CheckCompressionFieldStressInclinedShearReinforcement:
    """Validation for formula 8.60 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "expected", "expected_lhs"),
        [
            # 2 * (1 + 2^2) / (2 + cot(60)) = 10 / 2.577350, against a limit of 0.5 * 20 = 10
            (2.0, True, 3.87995381130102),
            # the same expression at three times the shear stress exceeds the limit
            (6.0, False, 11.63986143390306),
        ],
    )
    def test_evaluation(self, tau_ed: float, expected: bool, expected_lhs: float) -> None:
        """Tests the verdict and the stress that it is based on."""
        # Create object to test
        formula = Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(
            tau_ed=tau_ed,
            theta=THETA_COT_2,
            alpha_w=60.0,
            nu=0.5,
            f_cd=20.0,
        )

        # Perform test by assert
        assert bool(formula) is expected
        assert formula.lhs == pytest.approx(expected=expected_lhs, rel=1e-4)
        assert formula.rhs == pytest.approx(expected=10.0, rel=1e-4)

    def test_unity_check(self) -> None:
        """The unity check is the ratio of the compression field stress to its limit."""
        # Example values
        formula = Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(
            tau_ed=2.0,
            theta=THETA_COT_2,
            alpha_w=60.0,
            nu=0.5,
            f_cd=20.0,
        )

        assert formula.unity_check == pytest.approx(expected=0.387995381130102, rel=1e-4)

    def test_vertical_shear_reinforcement_recovers_formula_8_44(self) -> None:
        """alpha_w = 90 degrees lies outside the printed range of 45 <= alpha_w < 90, so this is a transcription
        check and not a supported use. There the cotangent vanishes and the expression collapses to
        tau_Ed * (cot(theta) + tan(theta)), which is the Formula (8.44) that (8.60) replaces.
        """
        # Example values
        formula = Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(
            tau_ed=2.0,
            theta=THETA_COT_2,
            alpha_w=90.0,
            nu=0.5,
            f_cd=20.0,
        )

        # 2 * (1 + 2^2) / 2 = 5, which equals 2 * (2 + 1/2)
        assert formula.lhs == pytest.approx(expected=5.0, rel=1e-4)

    def test_raise_error_when_the_shear_stress_is_negative(self) -> None:
        """Test if error is raised for the one parameter that may be zero but not negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(tau_ed=-2.0, theta=THETA_COT_2, alpha_w=60.0, nu=0.5, f_cd=20.0)

    @pytest.mark.parametrize(
        ("theta", "alpha_w"),
        [
            (-THETA_COT_2, 60.0),  # theta is negative
            (0.0, 60.0),  # theta is zero, for which the cotangent diverges
            (THETA_COT_2, -60.0),  # alpha_w is negative
            (THETA_COT_2, 0.0),  # alpha_w is zero, for which the cotangent diverges
        ],
    )
    def test_raise_error_when_the_angles_are_less_or_equal_to_zero(self, theta: float, alpha_w: float) -> None:
        """Test if error is raised for angles that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(tau_ed=2.0, theta=theta, alpha_w=alpha_w, nu=0.5, f_cd=20.0)

    @pytest.mark.parametrize(
        ("theta", "alpha_w"),
        [
            (120.0, 60.0),  # theta exceeds 90 degrees
            (THETA_COT_2, 120.0),  # alpha_w exceeds 90 degrees, which the standard says should be avoided
        ],
    )
    def test_raise_error_when_the_angles_exceed_90_degrees(self, theta: float, alpha_w: float) -> None:
        """Both angles are inclinations to the member axis, so neither can pass 90 degrees."""
        with pytest.raises(GreaterThan90Error):
            Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(tau_ed=2.0, theta=theta, alpha_w=alpha_w, nu=0.5, f_cd=20.0)

    @pytest.mark.parametrize(
        ("nu", "f_cd"),
        [
            (-0.5, 20.0),  # nu is negative
            (0.0, 20.0),  # nu is zero, which leaves the unity check without a denominator
            (0.5, -20.0),  # f_cd is negative
            (0.5, 0.0),  # f_cd is zero, which leaves the unity check without a denominator
        ],
    )
    def test_raise_error_when_the_limit_is_less_or_equal_to_zero(self, nu: float, f_cd: float) -> None:
        """The limit is the denominator of the unity check, so a zero one is rejected and not merely failed."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(tau_ed=2.0, theta=THETA_COT_2, alpha_w=60.0, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (
                2.0,
                "complete",
                (
                    r"CHECK \to \sigma_{cd} = \tau_{Ed} \cdot \frac{1 + \left(\cot(\theta)\right)^2}"
                    r"{\cot(\theta) + \cot(\alpha_w)} \leq \nu \cdot f_{cd} \to "
                    r"3.880 = 2.000 \cdot \frac{1 + \left(\cot(26.565)\right)^2}"
                    r"{\cot(26.565) + \cot(60.000)} \leq 0.500 \cdot 20.000 \to OK"
                ),
            ),
            (
                2.0,
                "complete_with_units",
                (
                    r"CHECK \to \sigma_{cd} = \tau_{Ed} \cdot \frac{1 + \left(\cot(\theta)\right)^2}"
                    r"{\cot(\theta) + \cot(\alpha_w)} \leq \nu \cdot f_{cd} \to "
                    r"3.880 \ MPa = 2.000 \ MPa \cdot \frac{1 + \left(\cot(26.565 ^\circ)\right)^2}"
                    r"{\cot(26.565 ^\circ) + \cot(60.000 ^\circ)} \leq 0.500 \cdot 20.000 \ MPa \to OK"
                ),
            ),
            (2.0, "short", r"CHECK \to OK"),
            (6.0, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(
            tau_ed=tau_ed,
            theta=THETA_COT_2,
            alpha_w=60.0,
            nu=0.5,
            f_cd=20.0,
        ).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
