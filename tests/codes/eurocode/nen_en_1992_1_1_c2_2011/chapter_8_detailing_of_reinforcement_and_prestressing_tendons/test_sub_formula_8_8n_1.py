"""Testing sub-formula 1 for 8.8N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8NConcreteStress,
    SubForm8Dot8NDesignLengthOfTransverseBar,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm8Dot8NDesignLengthOfTransverseBar:
    """Validation for sub-formula 8.8N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        phi_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = 100  # mm
        sub_form_8_8n_1 = SubForm8Dot8NDesignLengthOfTransverseBar(
            phi_t=phi_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )
        # Expected result, manually calculated
        manually_result = 53.578104
        assert sub_form_8_8n_1 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_evaluation_upper_limit(self) -> None:
        """Test the evaluation of the result if the upper limit is reached."""
        phi_t = 32  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = 50  # mm
        sub_form_8_8n_1 = SubForm8Dot8NDesignLengthOfTransverseBar(
            phi_t=phi_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )
        # Expected result, manually calculated
        manually_result = 50
        assert sub_form_8_8n_1 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_phi_t_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when phi_t is negative."""
        # Example values
        phi_t = -16  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = 100  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NDesignLengthOfTransverseBar(
                phi_t=phi_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_f_yd_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when f_yd is negative."""
        # Example values
        phi_t = 16  # mm
        f_yd = -500  # MPa
        sigma_td = 60  # MPa
        l_t = 100  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NDesignLengthOfTransverseBar(
                phi_t=phi_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_sigma_td_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when sigma_td is negative."""
        # Example values
        phi_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = -60  # MPa
        l_t = 100  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8NDesignLengthOfTransverseBar(
                phi_t=phi_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_sigma_td_is_zero(self) -> None:
        """Test if a NegativeValueError is raised when sigma_td is zero."""
        # Example values
        phi_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = 0  # MPa
        l_t = 100  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8NDesignLengthOfTransverseBar(
                phi_t=phi_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_raise_error_when_l_t_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when l_t is negative."""
        # Example values
        phi_t = 16  # mm
        f_yd = 500  # MPa
        sigma_td = 60  # MPa
        l_t = -100  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NDesignLengthOfTransverseBar(
                phi_t=phi_t,
                f_yd=f_yd,
                sigma_td=sigma_td,
                l_t=l_t,
            )

    def test_integration_with_sub_form_8_8n_concrete_stress(self) -> None:
        """Test the integration with sub-formula 8.8 for calculating concrete stress."""
        # Example values
        phi_t = 16  # mm
        f_yd = 500  # MPa
        l_t = 100  # mm
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y = 0.5  # -
        f_cd = 25  # MPa
        sigma_td = SubForm8Dot8NConcreteStress(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            y=y,
            f_cd=f_cd,
        )

        # Object to test
        form_8_8n = SubForm8Dot8NDesignLengthOfTransverseBar(
            phi_t=phi_t,
            f_yd=f_yd,
            sigma_td=sigma_td,
            l_t=l_t,
        )

        manually_calculated_result = 69.950631942

        assert form_8_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)
