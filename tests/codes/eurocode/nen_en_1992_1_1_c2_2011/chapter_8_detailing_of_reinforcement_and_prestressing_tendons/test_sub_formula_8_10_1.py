"""Testing sub formula 1 of formula 8.10 from EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_10 import (
    SubForm8Dot10Alpha6,
)
from blueprints.validations import NegativeValueError


class TestSubFormula8Dot8Alpha6:
    """Validation for sub formula 8.8 alpha 6 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        rho_1 = 32.5  # [-]
        sub_form_8_8_alpha_6 = SubForm8Dot10Alpha6(rho_1=rho_1)

        # manually calculated result
        manually_calculated_result = 1.140175  # [-]

        assert sub_form_8_8_alpha_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_minimum(self) -> None:
        """Test the evaluation of the result if the minimum is reached."""
        # example values
        rho_1 = 62.5  # [-]
        sub_form_8_8_alpha_6 = SubForm8Dot10Alpha6(rho_1=rho_1)

        # manually calculated result
        manually_calculated_result = 1.5  # [-]

        assert sub_form_8_8_alpha_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_maximum(self) -> None:
        """Test the evaluation of the result if the minimum is reached."""
        # example values
        rho_1 = 0.625  # [-]
        sub_form_8_8_alpha_6 = SubForm8Dot10Alpha6(rho_1=rho_1)

        # manually calculated result
        manually_calculated_result = 1  # [-]

        assert sub_form_8_8_alpha_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_negative_rho_1(self) -> None:
        """Test the evaluation of the result if rho_1 is negative."""
        # example values
        rho_1 = -0.01  # [-]

        with pytest.raises(NegativeValueError):
            SubForm8Dot10Alpha6(rho_1=rho_1)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"\alpha_6 = \max \left\{\min \left\{\left(\frac{\rho_1}{25}\right)^{0.5}; 1.5\right\}; 1\right\} = \max \left\{\min "
                r"\left\{\left(\frac{32.50}{25}\right)^{0.5}; 1.5\right\}; 1\right\} = 1.14",
            ),
            ("short", r"\alpha_6 = 1.14"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the LaTeX representation of the formula."""
        # example values
        rho_1 = 32.5

        latex = SubForm8Dot10Alpha6(rho_1=rho_1).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
