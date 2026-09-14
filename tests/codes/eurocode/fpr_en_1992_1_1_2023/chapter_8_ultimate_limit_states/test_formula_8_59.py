"""Testing formula 8.59 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_59 import (
    Form8Dot59ShearStressResistanceInclinedShearReinforcement,
)
from blueprints.validations import GreaterThan90Error, LessOrEqualToZeroError, NegativeValueError

# Angle chosen so that its cotangent is a round number, which keeps the hand calculations readable
THETA_COT_2 = 26.565051177078  # cot(theta) = 2


class TestForm8Dot59ShearStressResistanceInclinedShearReinforcement:
    """Validation for formula 8.59 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("alpha_w", "expected"),
        [
            # 0.002 * 435 * (2 + cot(60)) * sin(60) = 0.87 * 2.577350 * 0.866025
            (60.0, 1.9418842025849234),
            # alpha_w = 90 degrees lies outside the printed range of 45 <= alpha_w < 90, so this is a
            # transcription check and not a supported use: cot(90) = 0 and sin(90) = 1, so the formula
            # reproduces the (8.42) it replaces. Note that it cannot catch a misplaced cot(alpha_w), since
            # that term vanishes here; the case above is the discriminating one.
            (90.0, 1.74),
        ],
    )
    def test_evaluation(self, alpha_w: float, expected: float) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=0.002, f_ywd=435.0, theta=THETA_COT_2, alpha_w=alpha_w)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("rho_w", "f_ywd"),
        [
            (-0.002, 435.0),  # rho_w is negative
            (0.002, -435.0),  # f_ywd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, rho_w: float, f_ywd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=rho_w, f_ywd=f_ywd, theta=THETA_COT_2, alpha_w=60.0)

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
            Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=0.002, f_ywd=435.0, theta=theta, alpha_w=alpha_w)

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
            Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=0.002, f_ywd=435.0, theta=theta, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w) = "
                    r"0.002 \cdot 435.000 \cdot \left(\cot(26.565) + \cot(60.000)\right) \cdot \sin(60.000) = 1.942 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w) = "
                    r"0.002 \cdot 435.000 \ MPa \cdot \left(\cot(26.565 ^\circ) + \cot(60.000 ^\circ)\right) \cdot "
                    r"\sin(60.000 ^\circ) = 1.942 \ MPa"
                ),
            ),
            ("short", r"\tau_{Rd,sy} = 1.942 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=0.002, f_ywd=435.0, theta=THETA_COT_2, alpha_w=60.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
