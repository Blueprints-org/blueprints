"""Testing formula 8.9 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_9 import (
    Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter:
    """Validation for formula 8.9 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        f_wd = 15  # kN
        phi_t = 8  # mm
        phi_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa
        form_8_9 = Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
            f_wd=f_wd,
            phi_t=phi_t,
            phi_l=phi_l,
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
        phi_t = 8  # mm
        phi_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa
        form_8_9 = Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
            f_wd=f_wd,
            phi_t=phi_t,
            phi_l=phi_l,
            a_s=a_s,
            f_cd=f_cd,
        )

        manually_calculated_result = 20.096  # kN

        assert form_8_9 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_if_error_is_raised_for_negative_f_wd(self) -> None:
        """Test if the correct error is raised for a negative f_wd."""
        # example values
        f_wd = -15  # kN
        phi_t = 8  # mm
        phi_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                phi_t=phi_t,
                phi_l=phi_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_phi_t(self) -> None:
        """Test if the correct error is raised for a negative phi_t."""
        # example values
        f_wd = 15  # kN
        phi_t = -8  # mm
        phi_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                phi_t=phi_t,
                phi_l=phi_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_phi_l(self) -> None:
        """Test if the correct error is raised for a negative phi_l."""
        # example values
        f_wd = 15  # kN
        phi_t = 8  # mm
        phi_l = -10  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                phi_t=phi_t,
                phi_l=phi_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_zero_phi_l(self) -> None:
        """Test if the correct error is raised for a zero phi_l."""
        # example values
        f_wd = 15  # kN
        phi_t = 8  # mm
        phi_l = 0  # mm
        a_s = 78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                phi_t=phi_t,
                phi_l=phi_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_a_s(self) -> None:
        """Test if the correct error is raised for a negative a_s."""
        # example values
        f_wd = 15  # kN
        phi_t = 8  # mm
        phi_l = 10  # mm
        a_s = -78.5  # mm²
        f_cd = 20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                phi_t=phi_t,
                phi_l=phi_l,
                a_s=a_s,
                f_cd=f_cd,
            )

    def test_if_error_is_raised_for_negative_f_cd(self) -> None:
        """Test if the correct error is raised for a negative f_cd."""
        # example values
        f_wd = 15  # kN
        phi_t = 8  # mm
        phi_l = 10  # mm
        a_s = 78.5  # mm²
        f_cd = -20  # MPa

        with pytest.raises(NegativeValueError):
            Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(
                f_wd=f_wd,
                phi_t=phi_t,
                phi_l=phi_l,
                a_s=a_s,
                f_cd=f_cd,
            )
