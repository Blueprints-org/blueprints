"""Testing formula 3.25 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot25IncreasedCharacteristicCompressiveStrength


class TestForm3Dot24IncreasedCharacteristicCompressiveStrength:
    """Validation for formula 3.25 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.08 * f_ck  # MPa

        form_3_24 = Form3Dot25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2)

        # Expected result, manually calculated
        manually_calculated_result = 16.165

        assert form_3_24 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = -12.2  # MPa
        sigma_2 = 0.08 * f_ck  # MPa

        with pytest.raises(ValueError):
            Form3Dot25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2)

    def test_raise_error_when_sigma_2_is_smaller_than_0_05_f_ck(self) -> None:
        """Test a too small value."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.04 * f_ck  # MPa

        with pytest.raises(ValueError):
            Form3Dot25IncreasedCharacteristicCompressiveStrength(f_ck=f_ck, sigma_2=sigma_2)
