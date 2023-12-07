"""Testing formula 9.2 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_2 import Form9Dot2ShiftInMomentDiagram
from blueprints.validations import NegativeValueError


class TestForm9Dot2ShiftInMomentDiagram:
    """Validation for formula 9.2 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        z = 250  # mm
        theta = 30  # deg
        alpha = 85  # deg
        form_9_2 = Form9Dot2ShiftInMomentDiagram(z=z, theta=theta, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 205.570268

        assert form_9_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_z_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        z = -250  # mm
        theta = 30  # deg
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot2ShiftInMomentDiagram(z=z, theta=theta, alpha=alpha)

    def test_raise_error_when_alpha_is_zero(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        z = 250  # mm
        theta = 30  # deg
        alpha = 0  # deg

        with pytest.raises(ValueError):
            Form9Dot2ShiftInMomentDiagram(z=z, theta=theta, alpha=alpha)

    def test_raise_error_when_theta_is_zero(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        z = 250  # mm
        theta = 0  # deg
        alpha = 90  # deg

        with pytest.raises(ValueError):
            Form9Dot2ShiftInMomentDiagram(z=z, theta=theta, alpha=alpha)
