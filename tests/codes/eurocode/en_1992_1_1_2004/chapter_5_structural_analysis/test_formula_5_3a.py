"""Testing formula 5.3a of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_3a import Form5Dot3aTransverseForceUnbracedMembers
from blueprints.validations import NegativeValueError


class TestForm5Dot3aTransverseForceUnbracedMembers:
    """Validation for formula 5.3a from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_axial_force = 5  # kN

        # Object to test
        form_5_3a = Form5Dot3aTransverseForceUnbracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)

        # Expected result, manually calculated
        manually_calculated_result = 0.015  # kN

        assert form_5_3a == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("theta_i", "n_axial_force"),
        [
            (-0.003, 5),
            (0.003, -5),
        ],
    )
    def test_raise_error_when_negative_theta_i_is_given(self, theta_i: float, n_axial_force: float) -> None:
        """Test negative values."""
        with pytest.raises(NegativeValueError):
            Form5Dot3aTransverseForceUnbracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"H_i = \theta_i \cdot N = 0.003 \cdot 5.000 = 0.015",
            ),
            ("short", r"H_i = 0.015"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_i = 0.003  # -
        n_axial_force = 5  # kN

        # Object to test
        form_5_3a_latex = Form5Dot3aTransverseForceUnbracedMembers(theta_i=theta_i, n_axial_force=n_axial_force).latex()

        actual = {
            "complete": form_5_3a_latex.complete,
            "short": form_5_3a_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
