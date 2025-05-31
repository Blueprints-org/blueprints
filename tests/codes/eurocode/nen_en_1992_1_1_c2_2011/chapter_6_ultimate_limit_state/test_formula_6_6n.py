"""Testing formula 6.6n of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_6n import Form6Dot6nStrengthReductionFactor
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot6nStrengthReductionFactor:
    """Validation for formula 6.6n from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 30.0

        # Object to test
        formula = Form6Dot6nStrengthReductionFactor(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.528

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_ck"),
        [
            (-30.0),  # f_ck is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot6nStrengthReductionFactor(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\nu = 0.6 \cdot \left(1 - \frac{f_{ck}}{250}\right) = 0.6 \cdot \left(1 - \frac{30.000}{250}\right) = 0.528 \ -",
            ),
            ("short", r"\nu = 0.528 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30.0

        # Object to test
        latex = Form6Dot6nStrengthReductionFactor(f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
