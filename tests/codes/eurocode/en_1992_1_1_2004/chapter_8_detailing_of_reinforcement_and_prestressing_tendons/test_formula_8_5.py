"""Testing formula 8.5 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_5 import (
    Form8Dot5ProductAlphas235,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot4DesignAnchorageLength:
    """Validation for formula 8.5 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_2 = 0.8  # [-]
        alpha_3 = 0.9  # [-]
        alpha_5 = 1  # [-]
        form_8_4 = Form8Dot5ProductAlphas235(
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
        )

        # manually calculated result
        manually_calculated_result = 0.72  # mm

        assert form_8_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_below_minimum(self) -> None:
        """Test the evaluation of the result if the minimum is reached."""
        # example values
        alpha_2 = 0.6  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        form_8_4 = Form8Dot5ProductAlphas235(
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
        )

        # manually calculated result
        manually_calculated_result = 0.7  # mm

        assert form_8_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha_2", "alpha_3", "alpha_5"),
        [
            (-1, 1, 1),  # alpha_2 is negative
            (1, -1, 1),  # alpha_3 is negative
            (1, 1, -1),  # alpha_5 is negative
        ],
    )
    def test_negative_alpha(self, alpha_2: float, alpha_3: float, alpha_5: float) -> None:
        """Test the evaluation of the result if one of the alpha values is negative."""
        with pytest.raises(NegativeValueError):
            Form8Dot5ProductAlphas235(
                alpha_2=alpha_2,
                alpha_3=alpha_3,
                alpha_5=alpha_5,
            )

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"\alpha_2 \alpha_3 \alpha_5 \to \alpha_2 \cdot \alpha_3 \cdot \alpha_5 \ge 0.7 \to 1 \cdot 1 \cdot 1 \ge 0.7 \to 1.00"),
            ("short", r"\alpha_2 \alpha_3 \alpha_5 \to 1.00"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test latex representation of the formula."""
        alpha_2 = 1  # [-]
        alpha_3 = 1  # [-]
        alpha_5 = 1  # [-]
        latex = Form8Dot5ProductAlphas235(
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
