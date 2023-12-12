"""Testing sub-formula 2 for 8.8N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_8n import (
    SubForm8Dot8NFunctionX,
    SubForm8Dot8NFunctionY,
)
from blueprints.validations import NegativeValueError


class TestSubForm8Dot8NFunctionY:
    """Validation for sub-formula 8.8N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        x = 2

        sub_form_8_8n_3 = SubForm8Dot8NFunctionY(x=x)

        # Expected result, manually calculated
        manually_result = 0.112675

        assert sub_form_8_8n_3 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_x_is_negative(self) -> None:
        """Test if a NegativeValueError is raised when x is negative."""
        # Example values
        x = -2

        with pytest.raises(NegativeValueError):
            SubForm8Dot8NFunctionY(x=x)

    def test_integration_with_sub_form_8_8n_function_x(self) -> None:
        """Test the integration with sub-formula 8.8 for calculating function x."""
        # Example values
        c = 60  # mm
        phi_t = 16  # mm
        x = SubForm8Dot8NFunctionX(c=c, phi_t=phi_t)
        sub_form_8_8n_3 = SubForm8Dot8NFunctionY(x=x)

        # Expected result, manually calculated
        manually_result = 0.045314993

        assert sub_form_8_8n_3 == pytest.approx(expected=manually_result, rel=1e-4)
