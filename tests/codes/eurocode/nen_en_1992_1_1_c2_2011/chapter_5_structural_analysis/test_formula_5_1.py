"""Testing formula 5.1 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_5_structural_analysis.formula_5_1 import (
    Form5Dot1Imperfections,
    SubForm5Dot1ReductionFactorLengthOrHeight,
    SubForm5Dot1ReductionFactorNumberOfMembers,
)
from blueprints.validations import NegativeValueError


class TestForm5Dot1Imperfections:
    """Validation for formula 5.1 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8
        alpha_m = 0.9

        # Object to test
        form_5_1 = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)

        # Expected result, manually calculated
        manually_calculated_result = 0.0036

        assert form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_0_is_given(self) -> None:
        """Test a negative value of Θ0."""
        # Example values
        theta_0 = -0.005
        alpha_h = 0.8
        alpha_m = 0.9

        with pytest.raises(NegativeValueError):
            Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)

    def test_raise_error_when_negative_alpha_h_is_given(self) -> None:
        """Test a negative value of αh."""
        # Example values
        theta_0 = 0.005
        alpha_h = -0.8
        alpha_m = 0.9

        with pytest.raises(NegativeValueError):
            Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)

    def test_raise_error_when_negative_alpha_m_is_given(self) -> None:
        """Test a negative value of αm."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8
        alpha_m = -0.9

        with pytest.raises(NegativeValueError):
            Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)

    def test_integration_with_sub_formula_5_1_reduction_factor_length_or_height(self) -> None:
        """Test the integration with sub-formula 5.1 for the reduction factor for length or height, αh."""
        # Example values
        theta_0 = 0.005
        alpha_h = SubForm5Dot1ReductionFactorLengthOrHeight(length=5.3)
        alpha_m = 0.9

        # Object to test
        form_5_1 = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)

        # Expected result, manually calculated
        manually_calculated_result = 0.003909

        assert form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_integration_with_sub_formula_5_1_reduction_factor_number_of_members(self) -> None:
        """Test the integration with sub-formula 5.1 for the reduction factor for number of members, αm."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8
        alpha_m = SubForm5Dot1ReductionFactorNumberOfMembers(members=3)

        # Object to test
        form_5_1 = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)

        # Expected result, manually calculated
        manually_calculated_result = 0.00326598

        assert form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)
