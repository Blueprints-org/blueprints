"""Testing sub-formula for 3.10 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_10 import SubForm3Dot10FictionalCrossSection


class TestSubForm3Dot10FictionalCrossSection:
    """Validation for sub-formula for 3.10 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        a_c = 42.5  # mm²
        u = 20.3  # mm
        sub_form_3_10 = SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u)

        # Expected result, manually calculated
        manually_calculated_result = 4.187192

        assert sub_form_3_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_a_c_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        a_c = -42.5  # mm²
        u = 20.3  # mm

        with pytest.raises(ValueError):
            SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u)

    def test_raise_error_when_negative_u_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        a_c = 42.5  # mm²
        u = -20.3  # mm

        with pytest.raises(ValueError):
            SubForm3Dot10FictionalCrossSection(a_c=a_c, u=u)
