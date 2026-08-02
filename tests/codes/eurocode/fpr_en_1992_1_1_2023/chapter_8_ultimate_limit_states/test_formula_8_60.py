"""Testing formula 8.60 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_60 import (
    Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


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
            cot_theta=2.0,
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
            cot_theta=2.0,
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
            cot_theta=2.0,
            alpha_w=90.0,
            nu=0.5,
            f_cd=20.0,
        )

        # 2 * (1 + 2^2) / 2 = 5, which equals 2 * (2 + 1/2)
        assert formula.lhs == pytest.approx(expected=5.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_ed", "cot_theta", "alpha_w", "nu", "f_cd"),
        [
            (-2.0, 2.0, 60.0, 0.5, 20.0),  # tau_ed is negative
            (2.0, -2.0, 60.0, 0.5, 20.0),  # cot_theta is negative
            (2.0, 2.0, 60.0, -0.5, 20.0),  # nu is negative
            (2.0, 2.0, 60.0, 0.5, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, tau_ed: float, cot_theta: float, alpha_w: float, nu: float, f_cd: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(tau_ed=tau_ed, cot_theta=cot_theta, alpha_w=alpha_w, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("tau_ed", "cot_theta", "alpha_w", "nu", "f_cd"),
        [
            (2.0, 2.0, -60.0, 0.5, 20.0),  # alpha_w is negative
            (2.0, 2.0, 0.0, 0.5, 20.0),  # alpha_w is zero, for which the cotangent is undefined
            # Above 90 degrees the cotangent turns negative and can take the denominator with it. The standard
            # says such angles should be avoided, and here the expression would silently return a negative stress.
            (2.0, 0.0, 120.0, 0.5, 20.0),
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, tau_ed: float, cot_theta: float, alpha_w: float, nu: float, f_cd: float) -> None:
        """Test if error is raised where a value or the denominator is not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(tau_ed=tau_ed, cot_theta=cot_theta, alpha_w=alpha_w, nu=nu, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (
                2.0,
                "complete",
                r"CHECK \to \sigma_{cd} = \tau_{Ed} \cdot \frac{1 + \left(\cot(\theta)\right)^2}"
                r"{\cot(\theta) + \cot(\alpha_w)} \leq \nu \cdot f_{cd} \to "
                r"3.880 = 2.000 \cdot \frac{1 + \left(2.000\right)^2}"
                r"{2.000 + \cot(60.000)} \leq 0.500 \cdot 20.000 \to OK",
            ),
            (
                2.0,
                "complete_with_units",
                r"CHECK \to \sigma_{cd} = \tau_{Ed} \cdot \frac{1 + \left(\cot(\theta)\right)^2}"
                r"{\cot(\theta) + \cot(\alpha_w)} \leq \nu \cdot f_{cd} \to "
                r"3.880 \ MPa = 2.000 \ MPa \cdot \frac{1 + \left(2.000\right)^2}"
                r"{2.000 + \cot(60.000 \ degrees)} \leq 0.500 \cdot 20.000 \ MPa \to OK",
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
            cot_theta=2.0,
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
