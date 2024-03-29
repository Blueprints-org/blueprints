"""Testing formula 9.7N of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_7n import Form9Dot7nMaximumDistanceBentUpBars
from blueprints.validations import GreaterThan90Error, NegativeValueError


class TestForm9Dot7nMaximumDistanceBentUpBars:
    """Validation for formula 9.7N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg
        form_9_7n = Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 65.24931981

        assert form_9_7n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test if error is raised when d is negative."""
        d = -100  # mm
        alpha = 85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test if error is raised when alpha is negative."""
        d = 100  # mm
        alpha = -85  # deg

        with pytest.raises(NegativeValueError):
            Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)

    def test_raise_error_when_alpha_is_greater_90(self) -> None:
        """Test if error is raised when alpha is negative."""
        d = 100  # mm
        alpha = 110  # deg

        with pytest.raises(GreaterThan90Error):
            Form9Dot7nMaximumDistanceBentUpBars(d=d, alpha=alpha)
