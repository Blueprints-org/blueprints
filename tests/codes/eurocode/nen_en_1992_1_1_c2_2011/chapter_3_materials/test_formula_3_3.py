"""Testing formula 3.3 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_3 import (
    Form3Dot3AxialTensileStrengthFromTensileSplittingStrength,
)


class TestForm3Dot3AxialTensileStrengthFromTensileSplittingStrength:
    """Validation for formula 3.3 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ct_sp = 3.4  # MPa
        form_3_3 = Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(f_ct_sp=f_ct_sp)

        # Expected result, manually calculated
        manually_calculated_result = 3.06

        assert form_3_3 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_ct_sp_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ct_sp = -3.4  # MPa

        with pytest.raises(ValueError):
            Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(f_ct_sp=f_ct_sp)
