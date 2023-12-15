"""Testing sub-formula 4 for 8.8N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8NFunctionX,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestSubForm8Dot8NFunctionX:
    """Validation for sub-formula 8.8N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        c = 60  # mm
        diameter_t = 16  # mm

        sub_form_8_8n_4 = SubForm8Dot8NFunctionX(c=c, diameter_t=diameter_t)

        # Expected result, manually calculated
        manually_result = 8.5

        assert sub_form_8_8n_4 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_c_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when c is negative."""
        # Example values
        c = -60  # mm
        diameter_t = 16  # mm

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NFunctionX(c=c, diameter_t=diameter_t)

    def test_raise_error_when_diameter_t_is_negative(self) -> None:
        """Test if a LessOrEqualToZeroError is raised when diameter_t is negative."""
        # Example values
        c = 60  # mm
        diameter_t = -16  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8NFunctionX(c=c, diameter_t=diameter_t)

    def test_raise_error_when_diameter_t_is_zero(self) -> None:
        """Test if a LessOrEqualToZeroError is raised when diameter_t is zero."""
        # Example values
        c = 60  # mm
        diameter_t = 0  # mm

        with pytest.raises(LessOrEqualToZeroError):
            SubForm8Dot8NFunctionX(c=c, diameter_t=diameter_t)
