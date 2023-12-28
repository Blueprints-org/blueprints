"""Testing formula 9.1N of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_1n import (
    Form9Dot1NMinimumTensileReinforcementBeam,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot1NMinimumTensileReinforcementBeam:
    """Validation for formula 9.1N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation_first_term_decisive(self) -> None:
        """Test the evaluation of the result, if the first term of the formula is decisive."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = 150  # mm
        form_9_1n = Form9Dot1NMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 780 / 71

        assert form_9_1n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_second_term_decisive(self) -> None:
        """Test the evaluation of the result, if the second term of the formula is decisive."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 540  # MPa
        b_t = 50  # mm
        d = 150  # mm
        form_9_1n = Form9Dot1NMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 39 / 4

        assert form_9_1n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ctm_is_given(self) -> None:
        """Test if error is raised when f_ctm is negative."""
        # Example values
        f_ctm = -2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = 150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1NMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    def test_raise_error_when_negative_f_yk_is_given(self) -> None:
        """Test if error is raised when f_yk is negative."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = -355  # MPa
        b_t = 50  # mm
        d = 150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1NMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    def test_raise_error_when_negative_b_t_is_given(self) -> None:
        """Test if error is raised when b_t is negative."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = -50  # mm
        d = 150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1NMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is raised when d is negative."""
        # Example values
        f_ctm = 2  # MPa
        f_yk = 355  # MPa
        b_t = 50  # mm
        d = -150  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot1NMinimumTensileReinforcementBeam(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)
