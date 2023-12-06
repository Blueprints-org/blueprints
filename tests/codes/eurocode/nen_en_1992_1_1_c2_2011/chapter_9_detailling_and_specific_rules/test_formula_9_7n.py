"""Testing formula 9.7N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_7n import Form9Dot7NMaximumDistanceBentUpBars


class TestForm9Dot7NMaximumDistanceBentUpBars:
    """Validation for formula 9.7N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 100  # mm
        alpha = 85  # deg
        form_9_7n = Form9Dot7NMaximumDistanceBentUpBars(d=d, alpha=alpha)

        # Expected result, manually calculated
        manually_calculated_result = 65.24931981

        assert form_9_7n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test the evaluation of the result."""
        d = -100  # mm
        alpha = 85  # deg

        with pytest.raises(ValueError):
            Form9Dot7NMaximumDistanceBentUpBars(d=d, alpha=alpha)
