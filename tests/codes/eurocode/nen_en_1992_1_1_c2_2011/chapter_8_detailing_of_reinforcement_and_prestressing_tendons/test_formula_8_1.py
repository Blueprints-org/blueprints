"""Testing formula 8.1 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_1 import (
    Form8Dot1RequiredMinimumMandrelDiameter,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot1RequiredMinimumMandrelDiameter:
    """Validation for formula 8.1 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_bt = 80  # kN
        a_b = 200  # mm
        diameter = 16  # mm
        f_cd = 30  # MPa
        form_8_1 = Form8Dot1RequiredMinimumMandrelDiameter(
            f_bt=f_bt,
            a_b=a_b,
            diameter=diameter,
            f_cd=f_cd,
        )
        # Expected result, manually calculated
        manually_calculated_result = 290 / 3

        assert form_8_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_bt_is_given(self) -> None:
        """Tests if NegativeValueError is raised when f_bt is negative."""
        # Example values
        f_bt = -80  # kN
        a_b = 200  # mm
        diameter = 16  # mm
        f_cd = 30  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot1RequiredMinimumMandrelDiameter(
                f_bt=f_bt,
                a_b=a_b,
                diameter=diameter,
                f_cd=f_cd,
            )

    def test_raise_error_when_negative_a_b_is_given(self) -> None:
        """Tests if NegativeValueError is raised when a_b is negative."""
        # Example values
        f_bt = 80  # kN
        a_b = -200  # mm
        diameter = 16  # mm
        f_cd = 30  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot1RequiredMinimumMandrelDiameter(
                f_bt=f_bt,
                a_b=a_b,
                diameter=diameter,
                f_cd=f_cd,
            )

    def test_raise_error_when_negative_diameter_is_given(self) -> None:
        """Tests if NegativeValueError is raised when diameter is negative."""
        # Example values
        f_bt = 80  # kN
        a_b = 200  # mm
        diameter = -16  # mm
        f_cd = 30  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot1RequiredMinimumMandrelDiameter(
                f_bt=f_bt,
                a_b=a_b,
                diameter=diameter,
                f_cd=f_cd,
            )

    def test_raise_error_when_negative_f_cd_is_given(self) -> None:
        """Tests if NegativeValueError is raised when f_cd is negative."""
        # Example values
        f_bt = 80  # kN
        a_b = 200  # mm
        diameter = 16  # mm
        f_cd = -30  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot1RequiredMinimumMandrelDiameter(
                f_bt=f_bt,
                a_b=a_b,
                diameter=diameter,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"Ø_{m,min} = \frac{F_{bt} \left( \frac{1}{a_b} + \frac{1}{2 \cdot Ø} \right) }{f_{cd}} "
                    r"= \frac{80.00 \cdot 1000 \cdot \left( \frac{1}{200.00} + \frac{1}{2 \cdot 16.00} \right)}{30.00} = 96.67"
                ),
            ),
            ("short", r"Ø_{m,min} = 96.67"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_bt = 80  # kN
        a_b = 200  # mm
        diameter = 16  # mm
        f_cd = 30  # MPa

        # Object to test
        form_8_1_latex = Form8Dot1RequiredMinimumMandrelDiameter(
            f_bt=f_bt,
            a_b=a_b,
            diameter=diameter,
            f_cd=f_cd,
        ).latex()

        actual = {"complete": form_8_1_latex.complete, "short": form_8_1_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
