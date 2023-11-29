"""Testing formula 3.9 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot9DryingShrinkage


class TestForm3Dot9DryingShrinkage:
    """Validation for formula 3.9 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_ds_tt_s = 0.25  # -
        k_h = 0.75  # -
        epsilon_cd_0 = 0.44  # -
        form_3_9 = Form3Dot9DryingShrinkage(beta_ds_tt_s=beta_ds_tt_s, k_h=k_h, epsilon_cd_0=epsilon_cd_0)

        # Expected result, manually calculated
        manually_calculated_result = 0.0825

        assert form_3_9 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_beta_ds_tt_s_is_given(self) -> None:
        """Test that an error is raised when beta_ds_tt_s is negative"""
        # Example values
        beta_ds_tt_s = -0.25  # -
        k_h = 0.75  # -
        epsilon_cd_0 = 0.44  # -

        with pytest.raises(ValueError):
            Form3Dot9DryingShrinkage(beta_ds_tt_s=beta_ds_tt_s, k_h=k_h, epsilon_cd_0=epsilon_cd_0)

    def test_raise_error_when_negative_k_h_is_given(self) -> None:
        """Test that an error is raised when k_h is negative"""
        # Example values
        beta_ds_tt_s = 0.25  # -
        k_h = -0.75  # -
        epsilon_cd_0 = 0.44  # -

        with pytest.raises(ValueError):
            Form3Dot9DryingShrinkage(beta_ds_tt_s=beta_ds_tt_s, k_h=k_h, epsilon_cd_0=epsilon_cd_0)
