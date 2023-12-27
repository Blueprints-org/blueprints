"""Testing formula 9.9 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_9 import Form9Dot9MaximumSpacingSeriesOfLinks
from blueprints.validations import NegativeValueError


class TestForm9Dot9MaximumSpacingSeriesOfLinks:
    """Validation for formula 9.9 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg
        form_9_9 = Form9Dot9MaximumSpacingSeriesOfLinks(d=d, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 81.56164976

        assert form_9_9 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is given when d is negative."""
        d = -100  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot9MaximumSpacingSeriesOfLinks(d=d, alpha=alpha)
