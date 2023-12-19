"""Testing sub-formula 2 for 8.8N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8NConcreteStress,
    SubForm8Dot8NFunctionY,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm8Dot8NConcreteStress:
    """Validation for sub-formula 8.8N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0.5  # -
        f_cd = 25  # MPa
        sub_form_8_8n_2 = SubForm8Dot8NConcreteStress(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            y_function=y_function,
            f_cd=f_cd,
        )
        # Expected result, manually calculated
        manually_result = 35.2
        assert sub_form_8_8n_2 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_evaluation_upper_limit(self) -> None:
        """Test the evaluation of the result if the upper limit is reached."""
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0.05  # -
        f_cd = 20  # MPa
        sub_form_8_8n_2 = SubForm8Dot8NConcreteStress(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            y_function=y_function,
            f_cd=f_cd,
        )
        # Expected result, manually calculated
        manually_result = 60
        assert sub_form_8_8n_2 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_f_ctd_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when f_ctd is negative."""
        # Example values
        f_ctd = -2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0.5  # -
        f_cd = 25  # MPa

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NConcreteStress(
                f_ctd=f_ctd,
                sigma_cm=sigma_cm,
                y_function=y_function,
                f_cd=f_cd,
            )

    def test_raise_error_when_sigma_cm_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when sigma_cm is negative."""
        # Example values
        f_ctd = 2.6  # MPa
        sigma_cm = -15  # MPa
        y_function = 0.5  # -
        f_cd = 25  # MPa

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NConcreteStress(
                f_ctd=f_ctd,
                sigma_cm=sigma_cm,
                y_function=y_function,
                f_cd=f_cd,
            )

    def test_raise_error_when_y_is_negative(self) -> None:
        """Test if a LessOrEqualToZeroError is raised when y is negative."""
        # Example values
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = -0.5  # -
        f_cd = 25  # MPa

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8NConcreteStress(
                f_ctd=f_ctd,
                sigma_cm=sigma_cm,
                y_function=y_function,
                f_cd=f_cd,
            )

    def test_raise_error_when_y_is_zero(self) -> None:
        """Test if a LessOrEqualToZeroError is raised when y is zero."""
        # Example values
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0  # -
        f_cd = 25  # MPa

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8NConcreteStress(
                f_ctd=f_ctd,
                sigma_cm=sigma_cm,
                y_function=y_function,
                f_cd=f_cd,
            )

    def test_raise_error_when_f_cd_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when f_cd is negative."""
        # Example values
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        y_function = 0.5  # -
        f_cd = -25  # MPa

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NConcreteStress(
                f_ctd=f_ctd,
                sigma_cm=sigma_cm,
                y_function=y_function,
                f_cd=f_cd,
            )

    def test_integration_with_sub_form_8_8n_function_y(self) -> None:
        """Test the integration with sub-formula 8.8 for calculating function y."""
        # Example values
        f_ctd = 2.6  # MPa
        sigma_cm = 15  # MPa
        f_cd = 50  # MPa
        x_function = 1.5  # -
        y_function = SubForm8Dot8NFunctionY(x_function=x_function)

        # Object to test
        sub_form_8_8n_2 = SubForm8Dot8NConcreteStress(
            f_ctd=f_ctd,
            sigma_cm=sigma_cm,
            y_function=y_function,
            f_cd=f_cd,
        )

        # Expected result, manually calculated
        manually_result = 144.412473

        assert sub_form_8_8n_2 == pytest.approx(expected=manually_result, rel=1e-4)
