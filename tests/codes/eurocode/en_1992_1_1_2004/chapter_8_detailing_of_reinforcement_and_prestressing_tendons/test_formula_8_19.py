"""Testing formula 8.19 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_19 import (
    Form8Dot19DispersionLength,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm8Dot19DispersionLength:
    """Validation for formula 8.19 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_pt = 10  # m
        d = 2  # m
        form_8_19 = Form8Dot19DispersionLength(l_pt=l_pt, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 10.198

        assert form_8_19 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_l_pt_is_given(self) -> None:
        """Test a negative value for l_pt."""
        # Example values
        l_pt = -10  # m
        d = 2  # m

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot19DispersionLength(l_pt=l_pt, d=d)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test a negative value for d."""
        # Example values
        l_pt = 10  # m
        d = -2  # m

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot19DispersionLength(l_pt=l_pt, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"l_{disp} = \sqrt{l_{pt}^2 + d^2} = \sqrt{10.000^2 + 2.000^2} = 10.198",
            ),
            ("short", r"l_{disp} = 10.198"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        l_pt = 10  # m
        d = 2  # m

        # Object to test
        form_8_19_latex = Form8Dot19DispersionLength(l_pt=l_pt, d=d).latex()

        actual = {
            "complete": form_8_19_latex.complete,
            "short": form_8_19_latex.short,
        }

        assert actual[representation] == expected, f"{representation} representation failed."
