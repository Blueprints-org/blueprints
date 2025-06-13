"""Testing formula 8.3 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_3 import (
    Form8Dot3RequiredAnchorageLength,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot3RequiredAnchorageLength:
    """Validation for formula 8.3 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        diameter = 12  # mm
        sigma_sd = 435  # MPA
        f_bd = 2.9  # MPA
        form_8_3 = Form8Dot3RequiredAnchorageLength(diameter=diameter, sigma_sd=sigma_sd, f_bd=f_bd)

        manually_calculated_result = 450  # mm

        assert form_8_3 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_negative_diameter(self) -> None:
        """Test that an error is raised when diameter is negative."""
        # example values
        diameter = -1  # mm
        sigma_sd = 435  # MPA
        f_bd = 2.9  # MPA

        with pytest.raises(NegativeValueError):
            Form8Dot3RequiredAnchorageLength(diameter=diameter, sigma_sd=sigma_sd, f_bd=f_bd)

    def test_raise_error_negative_sigma_sd(self) -> None:
        """Test that an error is raised when sigma_sd is negative."""
        # example values
        diameter = 12  # mm
        sigma_sd = -1  # MPA
        f_bd = 2.9  # MPA

        with pytest.raises(NegativeValueError):
            Form8Dot3RequiredAnchorageLength(diameter=diameter, sigma_sd=sigma_sd, f_bd=f_bd)

    def test_raise_error_negative_f_bd(self) -> None:
        """Test that an error is raised when f_bd is negative."""
        # example values
        diameter = 12  # mm
        sigma_sd = 435  # MPA
        f_bd = -1  # MPA

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot3RequiredAnchorageLength(diameter=diameter, sigma_sd=sigma_sd, f_bd=f_bd)

    def test_raise_error__zero_f_bd(self) -> None:
        """Test that an error is raised when f_bd is zero."""
        # example values
        diameter = 12  # mm
        sigma_sd = 435  # MPA
        f_bd = 0  # MPA

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot3RequiredAnchorageLength(diameter=diameter, sigma_sd=sigma_sd, f_bd=f_bd)

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            (
                "complete",
                r"l_{b,rqd} = \frac{Ø}{4} \cdot \frac{\sigma_{sd}}{f_{bd}} = \frac{12}{4} \cdot \frac{435}{2.9} = 450.000",
            ),
            ("short", "l_{b,rqd} = 450.000"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the LaTeX representation."""
        diameter = 12  # MPa
        f_bd = 2.9  # MPa
        sigma_sd = 435  # MPa

        latex = Form8Dot3RequiredAnchorageLength(diameter=diameter, f_bd=f_bd, sigma_sd=sigma_sd).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
