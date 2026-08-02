"""Testing formula 8.59 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_59 import (
    Form8Dot59ShearStressResistanceInclinedShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot59ShearStressResistanceInclinedShearReinforcement:
    """Validation for formula 8.59 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("cot_theta", "alpha_w", "expected"),
        [
            # 0.002 * 435 * (2 + cot(60)) * sin(60) = 0.87 * 2.577350 * 0.866025
            (2.0, 60.0, 1.9418842025849234),
            # alpha_w = 90 degrees lies outside the printed range of 45 <= alpha_w < 90, so this is a
            # transcription check and not a supported use: cot(90) = 0 and sin(90) = 1, so the formula
            # reproduces the (8.42) it replaces. Note that it cannot catch a misplaced cot(alpha_w), since
            # that term vanishes here; the case above is the discriminating one.
            (2.0, 90.0, 1.74),
        ],
    )
    def test_evaluation(self, cot_theta: float, alpha_w: float, expected: float) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=0.002, f_ywd=435.0, cot_theta=cot_theta, alpha_w=alpha_w)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        ("rho_w", "f_ywd", "cot_theta", "alpha_w"),
        [
            (-0.002, 435.0, 2.0, 60.0),  # rho_w is negative
            (0.002, -435.0, 2.0, 60.0),  # f_ywd is negative
            (0.002, 435.0, -2.0, 60.0),  # cot_theta is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, rho_w: float, f_ywd: float, cot_theta: float, alpha_w: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("rho_w", "f_ywd", "cot_theta", "alpha_w"),
        [
            (0.002, 435.0, 2.0, -60.0),  # alpha_w is negative
            (0.002, 435.0, 2.0, 0.0),  # alpha_w is zero, for which the cotangent is undefined
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, rho_w: float, f_ywd: float, cot_theta: float, alpha_w: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w) = "
                r"0.002 \cdot 435.000 \cdot \left(2.000 + \cot(60.000)\right) \cdot \sin(60.000) = 1.942 \ MPa",
            ),
            (
                "complete_with_units",
                r"\tau_{Rd,sy} = \rho_w \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w) = "
                r"0.002 \cdot 435.000 \ MPa \cdot \left(2.000 + \cot(60.000 \ degrees)\right) \cdot "
                r"\sin(60.000 \ degrees) = 1.942 \ MPa",
            ),
            ("short", r"\tau_{Rd,sy} = 1.942 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot59ShearStressResistanceInclinedShearReinforcement(rho_w=0.002, f_ywd=435.0, cot_theta=2.0, alpha_w=60.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
