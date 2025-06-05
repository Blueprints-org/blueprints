"""Testing formula 8.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_14 import (
    Form8Dot14EquivalentDiameterBundledBars,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot14EquivalentDiameterBundledBars:
    """Validation for formula 8.14 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        diameter = 16  # mm
        n_b = 4  # [-]
        form_8_14 = Form8Dot14EquivalentDiameterBundledBars(diameter=diameter, n_b=n_b)

        # manually calculated result
        manually_calculated_result = 32  # mm

        assert form_8_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_maximum(self) -> None:
        """Test the evaluation of the result if the maximum is reached."""
        # example values
        diameter = 32  # mm
        n_b = 4  # [-]
        form_8_14 = Form8Dot14EquivalentDiameterBundledBars(diameter=diameter, n_b=n_b)

        # manually calculated result
        manually_calculated_result = 55  # mm

        assert form_8_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_diameter_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if diameter is negative."""
        # example values
        diameter = -32  # mm
        n_b = 4  # [-]

        with pytest.raises(NegativeValueError):
            Form8Dot14EquivalentDiameterBundledBars(diameter=diameter, n_b=n_b)

    def test_raise_error_if_n_b_is_negative(self) -> None:
        """Test that a NegativeValueError is raised if n_b is negative."""
        # example values
        diameter = 32
        n_b = -4

        with pytest.raises(NegativeValueError):
            Form8Dot14EquivalentDiameterBundledBars(diameter=diameter, n_b=n_b)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"Ø_n = \min \left(55 \ \text{mm}, Ø \cdot \sqrt{n_b} \right) = \min \left(55 \ \text{mm}, 16.00 \cdot \sqrt{4.00} \right) = 32.00"),
            ),
            ("short", r"Ø_n = 32.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        diameter = 16  # mm
        n_b = 4  # [-]

        # Object to test
        form_8_14_latex = Form8Dot14EquivalentDiameterBundledBars(diameter=diameter, n_b=n_b).latex()

        actual = {"complete": form_8_14_latex.complete, "short": form_8_14_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
