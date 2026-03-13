"""Testing formula 5.38a of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_38a import Form5Dot38aCheckRelativeSlendernessRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm5Dot38aCheckRelativeSlendernessRatio:
    """Validation for formula 5.38a from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        lambda_y = 1.0
        lambda_z = 1.5

        # Object to test
        formula = Form5Dot38aCheckRelativeSlendernessRatio(lambda_y=lambda_y, lambda_z=lambda_z)

        # Expected result, manually calculated
        expected_result = True

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("lambda_y", "lambda_z"),
        [
            (-1.0, 1.5),  # lambda_y is negative
            (1.0, -1.5),  # lambda_z is negative
            (0.0, 1.5),  # lambda_y is zero
            (1.0, 0.0),  # lambda_z is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, lambda_y: float, lambda_z: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form5Dot38aCheckRelativeSlendernessRatio(lambda_y=lambda_y, lambda_z=lambda_z)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{\lambda_{y}}{\lambda_{z}} \leq 2 \text{ and } \frac{\lambda_{z}}{\lambda_{y}} \leq 2 \right) \to "
                r"\left( \frac{1.000}{1.500} \leq 2 \text{ and } \frac{1.500}{1.000} \leq 2 \right) \to OK",
            ),
            ("short", r"CHECK \to OK"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        lambda_y = 1.0
        lambda_z = 1.5

        # Object to test
        latex = Form5Dot38aCheckRelativeSlendernessRatio(lambda_y=lambda_y, lambda_z=lambda_z).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
