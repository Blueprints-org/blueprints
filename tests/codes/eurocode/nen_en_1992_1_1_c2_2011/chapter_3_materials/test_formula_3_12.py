"""Testing formula 3.12 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot12AutogeneShrinkageInfinity


class TestForm3Dot11AutogeneShrinkage:
    """Validation for formula 3.12 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_ck = 15.8  # MPa
        form_3_12 = Form3Dot12AutogeneShrinkageInfinity(f_ck=f_ck)

        # Expected result, manually calculated
        manually_calculated_result = 1.45e-5

        assert form_3_12 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_f_ck_is_given(self) -> None:
        """Test formula raising error by a negative value."""
        # Example values
        f_ck = -15.8  # MPa

        with pytest.raises(ValueError):
            Form3Dot12AutogeneShrinkageInfinity(f_ck=f_ck)
