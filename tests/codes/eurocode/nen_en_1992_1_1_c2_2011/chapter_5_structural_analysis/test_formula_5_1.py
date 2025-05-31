"""Testing formula 5.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_1 import (
    Form5Dot1Imperfections,
    SubForm5Dot1ReductionFactorLengthOrHeight,
    SubForm5Dot1ReductionFactorNumberOfMembers,
)
from blueprints.validations import NegativeValueError


class TestForm5Dot1Imperfections:
    """Validation for formula 5.1 from EN 1992-1-1:2004."""

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

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha_m = \sqrt{0.5 \cdot ( 1 + 1 / m)} = \sqrt{0.5 \cdot ( 1 + 1 / 3.000)} = 0.816",
            ),
            ("short", r"\alpha_m = 0.816"),
        ],
    )
    def test_latex_sub2(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        members = 3

        # Object to test
        form_5_1_sub2_latex = SubForm5Dot1ReductionFactorNumberOfMembers(members).latex()

        actual = {
            "complete": form_5_1_sub2_latex.complete,
            "short": form_5_1_sub2_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha_h = \min( \max(2 / \sqrt{l}; 2/3); 1) = \min( \max(2 / \sqrt{5.300}; 2/3); 1) = 0.869",
            ),
            ("short", r"\alpha_h = 0.869"),
        ],
    )
    def test_latex_sub1(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        length = 5.3

        # Object to test
        form_5_1_sub1_latex = SubForm5Dot1ReductionFactorLengthOrHeight(length).latex()

        actual = {
            "complete": form_5_1_sub1_latex.complete,
            "short": form_5_1_sub1_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\theta_i = \theta_0 \cdot \alpha_h \cdot \alpha_m = 0.005 \cdot 0.800 \cdot 0.900 = 0.0036",
            ),
            ("short", r"\theta_i = 0.0036"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8
        alpha_m = 0.9

        # Object to test
        form_5_1_latex = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m).latex()

        actual = {
            "complete": form_5_1_latex.complete,
            "short": form_5_1_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
