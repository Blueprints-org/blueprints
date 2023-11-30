"""Testing formula 3.26 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot26IncreasedStrainAtMaxStrength


class TestForm3Dot26IncreasedStrainAtMaxStrength:
    """Validation for formula 3.26 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        f_ck_c = 14.08  # MPa
        epsilon_c2 = 0.33  # -

        form_3_26 = Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2)

        # Expected result, manually calculated
        manually_calculated_result = 0.43954

        assert form_3_26 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = -12.2  # MPa
        f_ck_c = 14.08  # MPa
        epsilon_c2 = 0.33  # -

        with pytest.raises(ValueError):
            Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2)

    def test_raise_error_when_negative_f_ck_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = 12.2  # MPa
        f_ck_c = -14.08  # MPa
        epsilon_c2 = 0.33  # -

        with pytest.raises(ValueError):
            Form3Dot26IncreasedStrainAtMaxStrength(f_ck=f_ck, f_ck_c=f_ck_c, epsilon_c2=epsilon_c2)
