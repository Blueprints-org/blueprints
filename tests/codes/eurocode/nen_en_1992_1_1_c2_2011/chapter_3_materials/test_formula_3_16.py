"""Testing formula 3.16 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_16 import Form3Dot16DesignValueTensileStrength


class TestForm3Dot16DesignValueTensileStrength:
    """Validation for formula 3.16 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        alpha_ct = 1.0  # -
        f_ctk_0_05 = 10.5  # MPa
        gamma_c = 0.8

        form_3_16 = Form3Dot16DesignValueTensileStrength(alpha_ct=alpha_ct, f_ctk_0_05=f_ctk_0_05, gamma_c=gamma_c)

        # Expected result, manually calculated
        manually_calculated_result = 13.125

        assert form_3_16 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_ct = -1.0  # -
        f_ctk_0_05 = 10.5  # MPa
        gamma_c = 0.8

        with pytest.raises(ValueError):
            Form3Dot16DesignValueTensileStrength(alpha_ct=alpha_ct, f_ctk_0_05=f_ctk_0_05, gamma_c=gamma_c)

    def test_raise_error_when_negative_f_ctk_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_ct = 1.0  # -
        f_ctk_0_05 = -10.5  # MPa
        gamma_c = 0.8

        with pytest.raises(ValueError):
            Form3Dot16DesignValueTensileStrength(alpha_ct=alpha_ct, f_ctk_0_05=f_ctk_0_05, gamma_c=gamma_c)

    def test_raise_error_when_negative_gamma_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_ct = 1.0  # -
        f_ctk_0_05 = 10.5  # MPa
        gamma_c = -0.8

        with pytest.raises(ValueError):
            Form3Dot16DesignValueTensileStrength(alpha_ct=alpha_ct, f_ctk_0_05=f_ctk_0_05, gamma_c=gamma_c)
