"""Testing sub-formula 2 of 3.14 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_14 import SubForm3Dot14K


class TestSub2Form3Dot14K:
    """Validation for sub-formula 2 of 3.14 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        e_cm = 3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 6.7  # MPa

        sub_2_form_3_14 = SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm)

        # Expected result, manually calculated
        manually_calculated_result = 0.22238

        assert sub_2_form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_e_cm_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        e_cm = -3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 6.7  # MPa

        with pytest.raises(ValueError):
            SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm)

    def test_raise_error_when_negative_or_zero_f_cm_is_given(self) -> None:
        """Test formula raising error by a negative or zero value."""
        # Example values
        e_cm = 3.3  # MPa
        epsilon_c1 = 0.43  # -
        f_cm = 0  # MPa

        with pytest.raises(ValueError):
            SubForm3Dot14K(e_cm=e_cm, epsilon_c1=epsilon_c1, f_cm=f_cm)
