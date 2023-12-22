"""Testing formula 8.17 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_17 import (
    Form8Dot17DesignValueTransmissionLength1,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot17DesignValueTransmissionLength1:
    """Validation for formula 8.17 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        l_pt = 140  # mm
        form_8_17 = Form8Dot17DesignValueTransmissionLength1(l_pt=l_pt)
        # manually calculated result
        manually_calculated_result = 96  # mm

        assert form_8_17 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_negative_l_pt(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for l_pt."""
        l_pt = -1
        with pytest.raises(NegativeValueError):
            Form8Dot17DesignValueTransmissionLength1(l_pt=l_pt)
