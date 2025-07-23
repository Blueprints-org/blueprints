"""Testing formula 5.101 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_2_2005.chapter_5_structural_analysis.formula_5_101 import (
    Form5Dot101Imperfections,
    Form5Dot101Sub1ReductionFactorLengthOrHeight,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot101Imperfections:
    """Validation for formula 5.101 from EN 1992-2:2005."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        theta_0 = 0.005
        alpha_h = 0.8

        # Object to test
        form_5_1 = Form5Dot101Imperfections(theta_0=theta_0, alpha_h=alpha_h)

        # Expected result, manually calculated
        manually_calculated_result = 0.004

        assert form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_theta_0_is_given(self) -> None:
        """Test a negative value of Θ0."""
        # Example values
        theta_0 = -0.005
        alpha_h = 0.8

        with pytest.raises(NegativeValueError):
            Form5Dot101Imperfections(theta_0=theta_0, alpha_h=alpha_h)

    def test_raise_error_when_negative_alpha_h_is_given(self) -> None:
        """Test a negative value of αh."""
        # Example values
        theta_0 = 0.005
        alpha_h = -0.8

        with pytest.raises(NegativeValueError):
            Form5Dot101Imperfections(theta_0=theta_0, alpha_h=alpha_h)

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
        form_5_1_latex = Form5Dot101Imperfections(theta_0=theta_0, alpha_h=alpha_h).latex()

        actual = {
            "complete": form_5_1_latex.complete,
            "short": form_5_1_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm5Dot101Sub1ReductionFactorLengthOrHeight:
    """Validation for subformula of 5.101 from EN 1992-2:2005."""

    @pytest.mark.parametrize(
        ("length", "expected"),
        [
            (5.3, 0.86874448552),  # Example value
            (0.683, 1),  # Example value where the result should be capped at 1
        ],
    )
    def test_evaluation_sub1(self, length: float, expected: float) -> None:
        """Test the evaluation of the result."""
        # Object to test
        form_5_1_sub1 = Form5Dot101Sub1ReductionFactorLengthOrHeight(length)

        assert form_5_1_sub1 == pytest.approx(expected=expected, rel=1e-4)

    @pytest.mark.parametrize(
        "length",
        [
            -5.3,  # length is negative
            0.0,  # length is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given_sub1(self, length: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot101Sub1ReductionFactorLengthOrHeight(length)

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
        form_5_1_sub1_latex = Form5Dot101Sub1ReductionFactorLengthOrHeight(length).latex()

        actual = {
            "complete": form_5_1_sub1_latex.complete,
            "short": form_5_1_sub1_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
