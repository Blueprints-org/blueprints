"""Testing formula 3.15 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_15 import Form3Dot15DesignValueCompressiveStrength


class TestForm3Dot15DesignValueCompressiveStrength:
    """Validation for formula 3.15 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = 0.8

        form_3_15 = Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

        # Expected result, manually calculated
        manually_calculated_result = 13.125

        assert form_3_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_alpha_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_cc = -1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = 0.8

        with pytest.raises(ValueError):
            Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = -10.5  # MPa
        gamma_c = 0.8

        with pytest.raises(ValueError):
            Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)

    def test_raise_error_when_negative_gamma_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        alpha_cc = 1.0  # -
        f_ck = 10.5  # MPa
        gamma_c = -0.8

        with pytest.raises(ValueError):
            Form3Dot15DesignValueCompressiveStrength(alpha_cc=alpha_cc, f_ck=f_ck, gamma_c=gamma_c)
