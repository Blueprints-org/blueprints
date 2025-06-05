"""Testing formula 8.16 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_16 import (
    Form8Dot16BasicTransmissionLength,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot16BasicTransmissionLength:
    """Validation for formula 8.16 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 0.25  # [-]
        diameter = 8  # mm
        sigma_pm0 = 350  # MPa
        f_bpt = 5  # MPa
        form_8_16 = Form8Dot16BasicTransmissionLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            diameter=diameter,
            sigma_pm0=sigma_pm0,
            f_bpt=f_bpt,
        )

        # manually calculated result
        manually_calculated_result = 140  # mm

        assert form_8_16 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_negative_alpha_1(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for alpha_1."""
        alpha_1 = -1
        alpha_2 = 1
        diameter = 8
        sigma_pm0 = 0.5
        f_bpt = 5
        with pytest.raises(NegativeValueError):
            Form8Dot16BasicTransmissionLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                diameter=diameter,
                sigma_pm0=sigma_pm0,
                f_bpt=f_bpt,
            )

    def test_raise_error_if_negative_alpha_2(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for alpha_2."""
        alpha_1 = 1
        alpha_2 = -1
        diameter = 8
        sigma_pm0 = 0.5
        f_bpt = 5
        with pytest.raises(NegativeValueError):
            Form8Dot16BasicTransmissionLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                diameter=diameter,
                sigma_pm0=sigma_pm0,
                f_bpt=f_bpt,
            )

    def test_raise_error_if_negative_diameter(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for diameter."""
        alpha_1 = 1
        alpha_2 = 1
        diameter = -8
        sigma_pm0 = 0.5
        f_bpt = 5
        with pytest.raises(NegativeValueError):
            Form8Dot16BasicTransmissionLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                diameter=diameter,
                sigma_pm0=sigma_pm0,
                f_bpt=f_bpt,
            )

    def test_raise_error_if_negative_sigma_pm0(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for sigma_pm0."""
        alpha_1 = 1
        alpha_2 = 1
        diameter = 8
        sigma_pm0 = -0.5
        f_bpt = 5
        with pytest.raises(NegativeValueError):
            Form8Dot16BasicTransmissionLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                diameter=diameter,
                sigma_pm0=sigma_pm0,
                f_bpt=f_bpt,
            )

    def test_raise_error_if_negative_f_bpt(self) -> None:
        """Test that a LessOrEqualToZeroError is raised when a negative value is passed for f_bpt."""
        alpha_1 = 1
        alpha_2 = 1
        diameter = 8
        sigma_pm0 = 0.5
        f_bpt = -5
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot16BasicTransmissionLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                diameter=diameter,
                sigma_pm0=sigma_pm0,
                f_bpt=f_bpt,
            )

    def test_raise_error_if_zero_f_bpt(self) -> None:
        """Test that a NegativeValueError is raised when a zero value is passed for f_bpt."""
        alpha_1 = 1
        alpha_2 = 1
        diameter = 8
        sigma_pm0 = 0.5
        f_bpt = 0
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot16BasicTransmissionLength(
                alpha_1=alpha_1,
                alpha_2=alpha_2,
                diameter=diameter,
                sigma_pm0=sigma_pm0,
                f_bpt=f_bpt,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"l_{pt} = \alpha_1 \cdot \alpha_2 \cdot Ø \cdot \frac{\sigma_{pm0}}{f_{bpt}} = "
                    r"1.00 \cdot 0.25 \cdot 8.00 \cdot \frac{350.00}{5.00} = 140.00"
                ),
            ),
            ("short", r"l_{pt} = 140.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        alpha_1 = 1  # [-]
        alpha_2 = 0.25  # [-]
        diameter = 8  # mm
        sigma_pm0 = 350  # MPa
        f_bpt = 5  # MPa

        # Object to test
        form_8_16_latex = Form8Dot16BasicTransmissionLength(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            diameter=diameter,
            sigma_pm0=sigma_pm0,
            f_bpt=f_bpt,
        ).latex()

        actual = {"complete": form_8_16_latex.complete, "short": form_8_16_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
