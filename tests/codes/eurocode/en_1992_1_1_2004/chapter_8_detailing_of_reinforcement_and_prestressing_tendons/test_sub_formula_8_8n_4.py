"""Testing sub-formula 4 for 8.8N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8nFunctionX,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm8Dot8nFunctionX:
    """Validation for sub-formula 8.8N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        cover = 60  # mm
        diameter_t = 16  # mm

        sub_form_8_8n_4 = SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t)

        # Expected result, manually calculated
        manually_result = 8.5

        assert sub_form_8_8n_4 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_c_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when c is negative."""
        # Example values
        cover = -60  # mm
        diameter_t = 16  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t)

    def test_raise_error_when_diameter_t_is_negative(self) -> None:
        """Test if a LessOrEqualToZeroError is raised when diameter_t is negative."""
        # Example values
        cover = 60  # mm
        diameter_t = -16  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t)

    def test_raise_error_when_diameter_t_is_zero(self) -> None:
        """Test if a LessOrEqualToZeroError is raised when diameter_t is zero."""
        # Example values
        cover = 60  # mm
        diameter_t = 0  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"x = 2 \cdot \frac{c}{Ø_t} = 2 \cdot \frac{60.00}{16.00} = 8.50"),
            ("short", r"x = 8.50"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        cover = 60  # mm
        diameter_t = 16  # mm

        # Object to test
        sub_form_8_8n_4_latex = SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t).latex()

        actual = {"complete": sub_form_8_8n_4_latex.complete, "short": sub_form_8_8n_4_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
