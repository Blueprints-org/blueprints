"""Testing formula 9.10 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_10 import Form9Dot10MaximumSpacingBentUpBars
from blueprints.validations import NegativeValueError


class TestForm9Dot10MaximumSpacingBentUpBars:
    """Validation for formula 9.10 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 200  # mm
        form_9_10 = Form9Dot10MaximumSpacingBentUpBars(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 200

        assert form_9_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is given when d is negative."""
        d = -200  # mm

        with pytest.raises(NegativeValueError):
            Form9Dot10MaximumSpacingBentUpBars(d=d)
