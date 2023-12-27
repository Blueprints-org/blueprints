"""Testing formula 3.13 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_13 import Form3Dot13CoefficientTimeAutogeneShrinkage


class TestForm3Dot13CoefficientTimeAutogeneShrinkage:
    """Validation for formula 3.13 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        t = 5  # days
        form_3_13 = Form3Dot13CoefficientTimeAutogeneShrinkage(t=t)

        # Expected result, manually calculated
        manually_calculated_result = 0.3605927

        assert form_3_13 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        t = -5  # days

        with pytest.raises(ValueError):
            Form3Dot13CoefficientTimeAutogeneShrinkage(t=t)
