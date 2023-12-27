"""Testing formula 5.3a of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_3a import Form5Dot3ATransverseForceUnbracedMembers
from blueprints.validations import NegativeValueError


class TestForm5Dot3ATransverseForceUnbracedMembers:
    """Validation for formula 5.3a from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_i = 0.003  # -
        n_axial_force = 5  # kN

        # Object to test
        form_5_3a = Form5Dot3ATransverseForceUnbracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)

        # Expected result, manually calculated
        manually_calculated_result = 0.015  # kN

        assert form_5_3a == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_i_is_given(self) -> None:
        """Test a negative value for theta_i."""
        # Example values
        theta_i = -0.003
        n_axial_force = 5

        with pytest.raises(NegativeValueError):
            Form5Dot3ATransverseForceUnbracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)

    def test_raise_error_when_negative_n_is_given(self) -> None:
        """Test a negative value for n."""
        # Example values
        theta_i = 0.003
        n_axial_force = -5

        with pytest.raises(NegativeValueError):
            Form5Dot3ATransverseForceUnbracedMembers(theta_i=theta_i, n_axial_force=n_axial_force)
