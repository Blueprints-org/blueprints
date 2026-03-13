"""Testing formula 5.24 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_24 import Form5Dot24AxialForceCorrectionFactor
from blueprints.validations import NegativeValueError


class TestForm5Dot24AxialForceCorrectionFactor:
    """Validation for formula 5.24 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n = 0.5  # -
        lambda_factor = 85  # -

        # Object to test
        form_5_24 = Form5Dot24AxialForceCorrectionFactor(n=n, lambda_factor=lambda_factor)

        # Expected result, manually calculated
        manually_calculated_result = 0.25  # -

        assert form_5_24 == pytest.approx(expected=min(manually_calculated_result, 0.20), rel=1e-4)

    def test_raise_error_when_negative_n_is_given(self) -> None:
        """Test a negative value for n."""
        # Example values
        n = -0.5
        lambda_factor = 85

        with pytest.raises(NegativeValueError):
            Form5Dot24AxialForceCorrectionFactor(n=n, lambda_factor=lambda_factor)

    def test_raise_error_when_negative_lambda_factor_is_given(self) -> None:
        """Test a negative value for lambda_factor."""
        # Example values
        n = 0.5
        lambda_factor = -85

        with pytest.raises(NegativeValueError):
            Form5Dot24AxialForceCorrectionFactor(n=n, lambda_factor=lambda_factor)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"k_2 = \min(0.20; n \cdot \frac{λ}{170}) = \min(0.20; 0.500 \cdot \frac{85.000}{170}) = 0.200"),
            ("short", "k_2 = 0.200"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n = 0.5  # -
        lambda_factor = 85  # -

        # Object to test
        form_5_24_latex = Form5Dot24AxialForceCorrectionFactor(
            n=n,
            lambda_factor=lambda_factor,
        ).latex()

        actual = {
            "complete": form_5_24_latex.complete,
            "short": form_5_24_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
