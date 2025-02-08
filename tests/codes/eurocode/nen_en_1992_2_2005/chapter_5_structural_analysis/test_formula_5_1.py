"""Testing formula 5.1 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_2_2005.chapter_5_structural_analysis.formula_5_1 import (
    Form5Dot1Imperfections,
    Form5Dot1Sub1ReductionFactorLengthOrHeight,
)
from blueprints.validations import NegativeValueError


class TestForm5Dot1Imperfections:
    """Validation for formula 5.1 from NEN-EN 1992-2:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8

        # Object to test
        form_5_1 = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h)

        # Expected result, manually calculated
        manually_calculated_result = 0.004

        assert form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_0_is_given(self) -> None:
        """Test a negative value of Θ0."""
        # Example values
        theta_0 = -0.005
        alpha_h = 0.8

        with pytest.raises(NegativeValueError):
            Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h)

    def test_raise_error_when_negative_alpha_h_is_given(self) -> None:
        """Test a negative value of αh."""
        # Example values
        theta_0 = 0.005
        alpha_h = -0.8

        with pytest.raises(NegativeValueError):
            Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h)

    def test_integration_with_sub_formula_5_1_reduction_factor_length_or_height(self) -> None:
        """Test the integration with sub-formula 5.1 for the reduction factor for length or height, αh."""
        # Example values
        theta_0 = 0.005
        alpha_h = Form5Dot1Sub1ReductionFactorLengthOrHeight(length=5.3)

        # Object to test
        form_5_1 = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h)

        # Expected result, manually calculated
        manually_calculated_result = 0.004343722427630694

        assert form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\alpha_h = \min(2 / \sqrt{l}, 1) = \min( 2 / \sqrt{5.300}, 1) = 0.869",
            ),
            ("short", r"\alpha_h = 0.869"),
        ],
    )
    def test_latex_sub1(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        length = 5.3

        # Object to test
        form_5_1_sub1_latex = Form5Dot1Sub1ReductionFactorLengthOrHeight(length).latex()

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
                r"\theta_i = \theta_0 \cdot \alpha_h = 0.005 \cdot 0.800 = 0.0040",
            ),
            ("short", r"\theta_i = 0.0040"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8

        # Object to test
        form_5_1_latex = Form5Dot1Imperfections(theta_0=theta_0, alpha_h=alpha_h).latex()

        actual = {
            "complete": form_5_1_latex.complete,
            "short": form_5_1_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
