"""Testing formula 9.13 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_13 import Form9Dot13TensileForceToBeAnchored
from blueprints.validations import NegativeValueError


class TestForm9Dot13TensileForceToBeAnchored:
    """Validation for formula 9.13 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        r = 100  # mm
        z_e = 50  # mm
        z_i = 20  # mm
        form_9_13 = Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

        # Expected result, manually calculated
        manually_calculated_result = 250

        assert form_9_13 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_r_is_given(self) -> None:
        """Test the evaluation of the result."""
        r = -100  # mm
        z_e = 50  # mm
        z_i = 20  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

    def test_raise_error_when_negative_z_e_is_given(self) -> None:
        """Test the evaluation of the result."""
        r = 100  # mm
        z_e = -50  # mm
        z_i = 20  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)

    def test_raise_error_when_negative_z_i_is_given(self) -> None:
        """Test the evaluation of the result."""
        r = 100  # mm
        z_e = 50  # mm
        z_i = -20  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot13TensileForceToBeAnchored(r=r, z_e=z_e, z_i=z_i)
