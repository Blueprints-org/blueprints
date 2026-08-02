"""Testing formula 8.61 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_61 import (
    Form8Dot61AdditionalTensileForceInclinedShearReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot61AdditionalTensileForceInclinedShearReinforcement:
    """Validation for formula 8.61 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("v_ed", "cot_theta", "alpha_w", "expected"),
        [
            # 300000 * (2 - cot(60)) = 300000 * 1.422650
            (300000.0, 2.0, 60.0, 426794.9192431122),
            # the standard takes the magnitude, so the sign of v_ed does not reach the result
            (-300000.0, 2.0, 60.0, 426794.9192431122),
            # alpha_w = 90 degrees lies outside the printed range of 45 <= alpha_w < 90, so this is a
            # transcription check and not a supported use: cot(90) = 0, which is the (8.50) it replaces
            (300000.0, 2.0, 90.0, 600000.0),
        ],
    )
    def test_evaluation(self, v_ed: float, cot_theta: float, alpha_w: float, expected: float) -> None:
        """Tests the evaluation of the result."""
        # Create object to test
        formula = Form8Dot61AdditionalTensileForceInclinedShearReinforcement(v_ed=v_ed, cot_theta=cot_theta, alpha_w=alpha_w)

        # Perform test by assert
        assert formula == pytest.approx(expected=expected, rel=1e-4)

    def test_result_is_not_clamped_at_zero(self) -> None:
        """Shear reinforcement inclined more steeply than the compression field gives a negative result. The
        standard prints no bound on it, so that value is returned unchanged rather than clamped.

        The values are chosen to sit inside the range that Formula (8.58) permits, so this is not an
        out of scope input: at alpha_w = 45 degrees the lower bound is tan(22.5) = 0.414, which lets
        cot_theta = 0.5 through, while cot(45) = 1 still exceeds it. At alpha_w = 60 degrees the two
        coincide at 1/sqrt(3), which would hide the sign entirely.
        """
        # Example values
        formula = Form8Dot61AdditionalTensileForceInclinedShearReinforcement(v_ed=300000.0, cot_theta=0.5, alpha_w=45.0)

        # the magnitude 300000 times the difference of 0.5 and cot(45) = 1.0
        assert formula == pytest.approx(expected=-150000.0, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "cot_theta", "alpha_w"),
        [
            (300000.0, -2.0, 60.0),  # cot_theta is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, v_ed: float, cot_theta: float, alpha_w: float) -> None:
        """Test if error is raised for parameters that are not allowed to be negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot61AdditionalTensileForceInclinedShearReinforcement(v_ed=v_ed, cot_theta=cot_theta, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("v_ed", "cot_theta", "alpha_w"),
        [
            (300000.0, 2.0, -60.0),  # alpha_w is negative
            (300000.0, 2.0, 0.0),  # alpha_w is zero, for which the cotangent is undefined
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero(self, v_ed: float, cot_theta: float, alpha_w: float) -> None:
        """Test if error is raised for parameters that are not allowed to be zero or less."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot61AdditionalTensileForceInclinedShearReinforcement(v_ed=v_ed, cot_theta=cot_theta, alpha_w=alpha_w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"N_{Vd} = \left|V_{Ed}\right| \cdot \left(\cot(\theta) - \cot(\alpha_w)\right) = "
                r"\left|300000.000\right| \cdot \left(2.000 - \cot(60.000)\right) = 426794.919 \ N",
            ),
            (
                "complete_with_units",
                r"N_{Vd} = \left|V_{Ed}\right| \cdot \left(\cot(\theta) - \cot(\alpha_w)\right) = "
                r"\left|300000.000 \ N\right| \cdot \left(2.000 - \cot(60.000 \ degrees)\right) = 426794.919 \ N",
            ),
            ("short", r"N_{Vd} = 426794.919 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        test_latex = Form8Dot61AdditionalTensileForceInclinedShearReinforcement(v_ed=300000.0, cot_theta=2.0, alpha_w=60.0).latex()

        actual = {
            "complete": test_latex.complete,
            "complete_with_units": test_latex.complete_with_units,
            "short": test_latex.short,
        }

        assert expected == actual[representation]
