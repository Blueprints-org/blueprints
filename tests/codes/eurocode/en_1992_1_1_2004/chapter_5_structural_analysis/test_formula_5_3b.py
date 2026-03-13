"""Testing formula 5.3b of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_1 import Form5Dot1Imperfections
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_3b import Form5Dot3bTransverseForceBracedMembers
from blueprints.validations import NegativeValueError


class TestForm5Dot3bTransverseForceBracedMembers:
    """Validation for formula 5.3b from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_axial_force = 5  # kN

        # Object to test
        form_5_3b = Form5Dot3bTransverseForceBracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)

        # Expected result, manually calculated
        manually_calculated_result = 0.030  # kN

        assert form_5_3b == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta_i", "n_axial_force"),
        [
            (-0.003, 5),
            (0.003, -5),
            (-0.003, -5),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, theta_i: float, n_axial_force: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot3bTransverseForceBracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)

    def test_integration_of_formulas_5_1_and_5_3b(self) -> None:
        """Test the integration of formulas 5.1 and 5.3b."""
        # Example values
        theta_0 = 0.005  # -
        alpha_m = 0.8  # -
        alpha_h = 0.9  # -
        n_axial_force = 5  # kN

        # Object to test
        form_5_3b = Form5Dot3bTransverseForceBracedMembers(
            theta_i=Form5Dot1Imperfections(theta_0=theta_0, alpha_m=alpha_m, alpha_h=alpha_h),
            n_axial_force=n_axial_force,
        )

        # Expected result, manually calculated
        manually_calculated_result = 0.036  # kN

        assert form_5_3b == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"H_{i} = 2\theta_{i}N = 2\cdot0.003\cdot5.000 = 0.030"),
            ("short", r"H_{i} = 0.030"),
            ("string", r"H_{i} = 2\theta_{i}N = 2\cdot0.003\cdot5.000 = 0.030"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        n_axial_force = 5  # kN

        # Object to test
        form_5_3b_latex = Form5Dot3bTransverseForceBracedMembers(theta_i=theta_i, n_axial_force=n_axial_force).latex()

        actual = {
            "complete": form_5_3b_latex.complete,
            "short": form_5_3b_latex.short,
            "string": str(form_5_3b_latex),
        }

        assert expected == actual[representation], f"{representation} representation."
