"""Testing formula 9.8N of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_8n import (
    Form9Dot8NMaximumTransverseDistanceLegsSeriesShearLinks,
)


class TestForm9Dot8NMaximumTransverseDistanceLegsSeriesShearLinks:
    """Validation for formula 9.8N from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 500  # mm
        form_9_8n = Form9Dot8NMaximumTransverseDistanceLegsSeriesShearLinks(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 375

        assert form_9_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_maximum_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        d = 1000  # mm
        form_9_8n = Form9Dot8NMaximumTransverseDistanceLegsSeriesShearLinks(d=d)

        # Expected result, manually calculated
        manually_calculated_result = 600

        assert form_9_8n == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_d_is_given(self) -> None:
        """Test the evaluation of the result."""
        d = -100  # mm

        with pytest.raises(ValueError):
            Form9Dot8NMaximumTransverseDistanceLegsSeriesShearLinks(d=d)
