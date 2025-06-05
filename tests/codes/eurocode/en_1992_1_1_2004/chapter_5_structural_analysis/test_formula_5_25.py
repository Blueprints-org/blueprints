"""Testing formula 5.25 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_25 import Form5Dot25AxialForceCorrectionFactor
from blueprints.validations import NegativeValueError


class TestForm5Dot25AxialForceCorrectionFactor:
    """Validation for formula 5.25 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        n = 0.5  # -

        # Object to test
        form_5_25 = Form5Dot25AxialForceCorrectionFactor(n=n)

        # Expected result, manually calculated
        manually_calculated_result = 0.15  # -

        assert form_5_25 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_n_is_given(self) -> None:
        """Test a negative value for n."""
        # Example values
        n = -0.5

        with pytest.raises(NegativeValueError):
            Form5Dot25AxialForceCorrectionFactor(n=n)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"k_{2} = \min(0.20; n \cdot 0.30) = \min(0.20; 0.500 \cdot 0.30) = 0.150"),
            ("short", "k_{2} = 0.150"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n = 0.5  # -

        # Object to test
        form_5_25_latex = Form5Dot25AxialForceCorrectionFactor(n=n).latex()

        actual = {
            "complete": form_5_25_latex.complete,
            "short": form_5_25_latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
