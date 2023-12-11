"""Testing formula 8.8n of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    Form8Dot8NAnchorageCapacityWeldedTransverseBar,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot8NForm8Dot8NAnchorageCapacityWeldedTransverseBar:
    """Validation for formula 8.8n from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_td = 100  # mm
        phi_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 400  # kN
        form_8_8n = Form8Dot8NAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            phi_t=phi_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 96

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_maximum(self) -> None:
        """Test the evaluation of the result if the maximum is reached."""
        # Example values
        l_td = 100  # mm
        phi_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 50  # kN
        form_8_8n = Form8Dot8NAnchorageCapacityWeldedTransverseBar(
            l_td=l_td,
            phi_t=phi_t,
            sigma_td=sigma_td,
            f_wd=f_wd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 50

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_l_td_is_given(self) -> None:
        """Test if NegativeValueError is raised when l_td is negative"""
        # Example values
        l_td = -100  # mm
        phi_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = 50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8NAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                phi_t=phi_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_raise_error_when_negative_phi_t_is_given(self) -> None:
        """Test if NegativeValueError is raised when phi_t is negative"""
        # Example values
        l_td = 100  # mm
        phi_t = -16  # mm
        sigma_td = 60  # MPa
        f_wd = 50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8NAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                phi_t=phi_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_raise_error_when_negative_sigma_td_is_given(self) -> None:
        """Test if NegativeValueError is raised when sigma_td is negative"""
        # Example values
        l_td = 100  # mm
        phi_t = 16  # mm
        sigma_td = -60  # MPa
        f_wd = 50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8NAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                phi_t=phi_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )

    def test_raise_error_when_negative_f_wd_is_given(self) -> None:
        """Test if NegativeValueError is raised when f_wd is negative"""
        # Example values
        l_td = 100  # mm
        phi_t = 16  # mm
        sigma_td = 60  # MPa
        f_wd = -50  # kN

        with pytest.raises(NegativeValueError):
            Form8Dot8NAnchorageCapacityWeldedTransverseBar(
                l_td=l_td,
                phi_t=phi_t,
                sigma_td=sigma_td,
                f_wd=f_wd,
            )
