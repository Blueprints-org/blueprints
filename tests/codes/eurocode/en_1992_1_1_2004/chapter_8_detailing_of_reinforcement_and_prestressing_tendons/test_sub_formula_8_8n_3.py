"""Testing sub-formula 3 for 8.8N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8nFunctionX,
    SubForm8Dot8nFunctionY,
)
from blueprints.validations import NegativeValueError


class TestSubForm8Dot8nFunctionY:
    """Validation for sub-formula 8.8N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        x_function = 2

        sub_form_8_8n_3 = SubForm8Dot8nFunctionY(x_function=x_function)

        # Expected result, manually calculated
        manually_result = 0.112675

        assert sub_form_8_8n_3 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_x_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when x is negative."""
        # Example values
        x_function = -2

        with pytest.raises(NegativeValueError):
            SubForm8Dot8nFunctionY(x_function=x_function)

    def test_integration_with_sub_form_8_8n_function_x(self) -> None:
        """Test the integration with sub-formula 8.8 for calculating function x."""
        # Example values
        cover = 60  # mm
        diameter_t = 16  # mm
        x_function = SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t)
        sub_form_8_8n_3 = SubForm8Dot8nFunctionY(x_function=x_function)

        # Expected result, manually calculated
        manually_result = 0.045314993

        assert sub_form_8_8n_3 == pytest.approx(expected=manually_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            ("complete", r"y = 0.015 + 0.14 \cdot e^{-0.18 \cdot x} = 0.015 + 0.14 \cdot e^{-0.18 \cdot 8.50} = 0.05"),
            ("short", r"y = 0.05"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        cover = 60  # mm
        diameter_t = 16  # mm
        x_function = SubForm8Dot8nFunctionX(cover=cover, diameter_t=diameter_t)

        # Object to test
        sub_form_8_8n_3_latex = SubForm8Dot8nFunctionY(x_function=x_function).latex()

        actual = {"complete": sub_form_8_8n_3_latex.complete, "short": sub_form_8_8n_3_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
