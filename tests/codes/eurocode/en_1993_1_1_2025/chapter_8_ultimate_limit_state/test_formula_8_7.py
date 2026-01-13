"""Testing formula 8.7 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_7 import Form8Dot7AdditionalMoment
from blueprints.validations import NegativeValueError


class TestForm8Dot7AdditionalMoment:
    """Validation for formula 8.7 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 1000.0
        e_n = 50.0

        # Object to test
        formula = Form8Dot7AdditionalMoment(n_ed=n_ed, e_n=e_n)

        # Expected result, manually calculated
        manually_calculated_result = 50000.0  # Nmm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "e_n"),
        [
            (-1000.0, 50.0),  # n_ed is negative
            (1000.0, -50.0),  # e_n is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, e_n: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot7AdditionalMoment(n_ed=n_ed, e_n=e_n)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta M_{Ed} = N_{Ed} \cdot e_{N} = 1000.000 \cdot 50.000 = 50000.000 \ Nmm",
            ),
            ("short", r"\Delta M_{Ed} = 50000.000 \ Nmm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 1000.0
        e_n = 50.0

        # Object to test
        latex = Form8Dot7AdditionalMoment(n_ed=n_ed, e_n=e_n).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
