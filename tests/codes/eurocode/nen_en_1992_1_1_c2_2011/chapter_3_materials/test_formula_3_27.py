"""Testing formula 3.27 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_27 import Form3Dot27IncreasedStrainLimitValue


class TestForm3Dot27IncreasedStrainLimitValue:
    """Validation for formula 3.27 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 12.2  # MPa
        sigma_2 = 0.08  # MPa
        epsilon_cu2 = 0.33  # -

        form_3_27 = Form3Dot27IncreasedStrainLimitValue(f_ck=f_ck, sigma_2=sigma_2, epsilon_cu2=epsilon_cu2)

        # Expected result, manually calculated
        manually_calculated_result = 0.331311

        assert form_3_27 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ck_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_ck = -12.2  # MPa
        sigma_2 = 0.08  # MPa
        epsilon_cu2 = 0.33  # -

        with pytest.raises(ValueError):
            Form3Dot27IncreasedStrainLimitValue(f_ck=f_ck, sigma_2=sigma_2, epsilon_cu2=epsilon_cu2)
