"""Testing formula 3.3 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot3AxialTensileStrengthFromTensileSplittingStrength

# pylint: disable=arguments-differ


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

    def test_raise_error_when_changing_value_after_initialization(self) -> None:
        """Test that an error is raised when changing a value after initialization."""
        # example values
        f_ct_sp = 3.4  # MPa
        form_3_3 = Form3Dot3AxialTensileStrengthFromTensileSplittingStrength(f_ct_sp=f_ct_sp)

        with pytest.raises(AttributeError):
            form_3_3.f_ct_sp = 2
