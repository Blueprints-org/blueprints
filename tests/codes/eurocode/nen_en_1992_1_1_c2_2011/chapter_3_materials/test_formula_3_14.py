"""Testing formula 3.14 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot14StressStrainForShortTermLoading


class TestForm3Dot14StressStrainForShortTermLoading:
    """Validation for formula 3.14 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        k = 0.38  # -
        eta = 0.88  # -
        form_3_14 = Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta)

        # Expected result, manually calculated
        manually_calculated_result = 1.03383

        assert form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_k_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        k = -0.38  # -
        eta = 0.88  # -

        with pytest.raises(ValueError):
            Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta)

    def test_raise_error_when_negative_eta_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        k = 0.38  # -
        eta = -0.88  # -

        with pytest.raises(ValueError):
            Form3Dot14StressStrainForShortTermLoading(k=k, eta=eta)
