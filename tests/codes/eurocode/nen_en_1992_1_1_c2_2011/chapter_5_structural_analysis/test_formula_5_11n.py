"""Testing formula 5.11n of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_11n import Form5Dot11nShearSlendernessCorrectionFactor
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot11nShearSlendernessCorrectionFactor:
    """Validation for formula 5.11N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        lambda_factor = 0.5  # -

        # Object to test
        form_5_11n = Form5Dot11nShearSlendernessCorrectionFactor(lambda_factor=lambda_factor)

        # Expected result, manually calculated
        manually_calculated_result = 0.40824  # -

        assert form_5_11n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "lambda_factor",
        [
            0,
            -0.3,
        ],
    )
    def test_raise_error_when_negative_values_or_zero_are_given(
        self,
        lambda_factor: float,
    ) -> None:
        """Test negative or zero values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot11nShearSlendernessCorrectionFactor(lambda_factor=lambda_factor)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"k_{λ} = \sqrt{\frac{λ}{3}} = \sqrt\frac{0.3}{3} = 0.316"),
            ("short", "k_{λ} = 0.316"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        lambda_factor = 0.3  # -

        # Object to test
        latex = Form5Dot11nShearSlendernessCorrectionFactor(lambda_factor=lambda_factor).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
