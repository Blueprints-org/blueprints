"""Testing formula 8.12 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_12 import (
    Form8Dot12AdditionalShearReinforcement,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot12AdditionalShearReinforcement:
    """Validation for formula 8.12 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        a_s = 100  # mm²
        n_1 = 2  # -
        form_8_12 = Form8Dot12AdditionalShearReinforcement(a_s=a_s, n_1=n_1)

        manually_calculated_result = 50  # mm²

        assert form_8_12 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_negative_a_s(self) -> None:
        """Test that an error is raised when a_s is negative."""
        # example values
        a_s = -100  # mm²
        n_1 = 2  # -

        with pytest.raises(NegativeValueError):
            Form8Dot12AdditionalShearReinforcement(a_s=a_s, n_1=n_1)

    def test_raise_error_negative_n_1(self) -> None:
        """Test that an error is raised when n_1 is negative."""
        # example values
        a_s = 100  # mm²
        n_1 = -2  # -

        with pytest.raises(NegativeValueError):
            Form8Dot12AdditionalShearReinforcement(a_s=a_s, n_1=n_1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"A_{sh} = 0.25 \cdot A_s \cdot n_1 = 0.25 \cdot 100.00 \cdot 2.00 = 50.00"),
            ("short", r"A_{sh} = 50.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        a_s = 100  # mm²
        n_1 = 2  # -

        # Object to test
        form_8_12_latex = Form8Dot12AdditionalShearReinforcement(a_s=a_s, n_1=n_1).latex()

        actual = {"complete": form_8_12_latex.complete, "short": form_8_12_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
