"""Testing formula 3.18 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_18 import Form3Dot18CompressiveStressConcrete


class TestForm3Dot17CompressiveStressConcrete:
    """Validation for formula 3.18 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_cd = 18.50  # MPa

        form_3_18 = Form3Dot18CompressiveStressConcrete(f_cd=f_cd)

        # Expected result, manually calculated
        manually_calculated_result = 18.50

        assert form_3_18 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_cd_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cd = -18.50  # MPa

        with pytest.raises(ValueError):
            Form3Dot18CompressiveStressConcrete(f_cd=f_cd)
