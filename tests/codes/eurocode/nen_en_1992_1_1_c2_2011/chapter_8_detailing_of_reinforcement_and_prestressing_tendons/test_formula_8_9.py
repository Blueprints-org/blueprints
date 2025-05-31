"""Testing formula 8.9 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_9 import (
    Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter:
    """Validation for formula 8.9 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        f_wd = 15  # kN
        diameter_t = 8  # mm
        diameter_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa
        form_8_9 = Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
            f_wd=f_wd,
            diameter_t=diameter_t,
            diameter_l=diameter_l,
            a_s=a_s,
            f_cd=f_cd,
        )

        manually_calculated_result = 15  # kN

        assert form_8_9 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_upper_limit(self) -> None:
        """Test the evaluation of the result if the upper limit is reached."""
        # example values
        # example values
        f_wd = 25  # kN
        diameter_t = 8  # mm
        diameter_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa
        form_8_9 = Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
            f_wd=f_wd,
            diameter_t=diameter_t,
            diameter_l=diameter_l,
            a_s=a_s,
            f_cd=f_cd,
        )

        manually_calculated_result = 20.096  # kN

        assert form_8_9 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_if_error_is_raised_for_negative_f_wd(self) -> None:
        """Test if the correct error is raised for a negative f_wd."""
        # example values
        f_wd = -15  # kN
        diameter_t = 8  # mm
        diameter_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                diameter_t=diameter_t,
                diameter_l=diameter_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_diameter_t(self) -> None:
        """Test if the correct error is raised for a negative diameter_t."""
        # example values
        f_wd = 15  # kN
        diameter_t = -8  # mm
        diameter_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                diameter_t=diameter_t,
                diameter_l=diameter_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_diameter_l(self) -> None:
        """Test if the correct error is raised for a negative diameter_l."""
        # example values
        f_wd = 15  # kN
        diameter_t = 8  # mm
        diameter_l = -10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                diameter_t=diameter_t,
                diameter_l=diameter_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_zero_diameter_l(self) -> None:
        """Test if the correct error is raised for a zero diameter_l."""
        # example values
        f_wd = 15  # kN
        diameter_t = 8  # mm
        diameter_l = 0  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                diameter_t=diameter_t,
                diameter_l=diameter_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_a_s(self) -> None:
        """Test if the correct error is raised for a negative a_s."""
        # example values
        f_wd = 15  # kN
        diameter_t = 8  # mm
        diameter_l = 10  # mm
        a_s = -78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                diameter_t=diameter_t,
                diameter_l=diameter_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_f_cd(self) -> None:
        """Test if the correct error is raised for a negative f_cd."""
        # example values
        f_wd = 15  # kN
        diameter_t = 8  # mm
        diameter_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = -20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                diameter_t=diameter_t,
                diameter_l=diameter_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"F_{btd} = \min \left( F_{wd}, 16 \cdot A_s \cdot f_{cd} \cdot \frac{Ø_t}{Ø_l} \right) = "
                    r"\min \left( 15.00, 1000 \cdot 16 \cdot 78.50 \cdot 20.00 \cdot \frac{8.00}{10.00} \right) = 15.00"
                ),
            ),
            ("short", r"F_{btd} = 15.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # example values
        f_wd = 15  # kN
        diameter_t = 8  # mm
        diameter_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        # Object to test
        form_8_9_latex = Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
            f_wd=f_wd,
            diameter_t=diameter_t,
            diameter_l=diameter_l,
            a_s=a_s,
            f_cd=f_cd,
        ).latex()

        actual = {"complete": form_8_9_latex.complete, "short": form_8_9_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
