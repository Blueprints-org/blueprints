"""Testing formula 3.21 and 22 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_21_22 import Form3Dot21And22EffectiveStrength


class TestForm3Dot19And20EffectivePressureZoneHeight:
    """Validation for formula 3.21 and 22 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation_1(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 18.50  # MPa

        form_3_21_22 = Form3Dot21And22EffectiveStrength(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 1.0

        assert form_3_21_22 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 83.5  # MPa

        form_3_21_22 = Form3Dot21And22EffectiveStrength(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 0.8325

        assert form_3_21_22 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_f_ck_is_larger_than_90(self) -> None:
        """Test a too large value."""
        # Example values
        f_ck = 105  # MPa

        with pytest.raises(ValueError):
            Form3Dot21And22EffectiveStrength(f_ck=f_ck)
