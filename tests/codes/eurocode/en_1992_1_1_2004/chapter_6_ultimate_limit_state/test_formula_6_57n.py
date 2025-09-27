"""Testing formula 6.57N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_57n import Form6Dot57nNuPrime
from blueprints.validations import NegativeValueError


class TestForm6Dot57nNuPrime:
    """Validation for formula 6.57N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_ck = 30.0

        # Object to test
        formula = Form6Dot57nNuPrime(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.88  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        "f_ck",
        [
            -30.0,  # f_ck is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, f_ck: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot57nNuPrime(f_ck=f_ck)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\nu' = 1 - \frac{f_{ck}}{250} = 1 - \frac{30.000}{250} = 0.880 \ -",
            ),
            ("short", r"\nu' = 0.880 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_ck = 30.0

        # Object to test
        latex = Form6Dot57nNuPrime(f_ck=f_ck).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
