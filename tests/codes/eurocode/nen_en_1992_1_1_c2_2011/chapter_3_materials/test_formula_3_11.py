"""Testing formula 3.11 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_11 import Form3Dot11AutogeneShrinkage


class TestForm3Dot11AutogeneShrinkage:
    """Validation for formula 3.11 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_as_t = 0.25  # -
        epsilon_ca_inf = 0.056  # -
        form_3_11 = Form3Dot11AutogeneShrinkage(beta_as_t=beta_as_t, epsilon_ca_inf=epsilon_ca_inf)

        # Expected result, manually calculated
        manually_calculated_result = 0.014

        assert form_3_11 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_beta_as_t_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        beta_as_t = -0.25  # -
        epsilon_ca_inf = 0.056  # -

        with pytest.raises(ValueError):
            Form3Dot11AutogeneShrinkage(beta_as_t=beta_as_t, epsilon_ca_inf=epsilon_ca_inf)
