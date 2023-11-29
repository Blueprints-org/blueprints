"""Testing sub-formula for 3.2 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import SubForm3Dot2CoefficientTypeOfCementS


class TestSubForm3Dot2CoefficientTypeOfCementS:
    """Validation for formula 3.2 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        cement_class = "R"  # str
        sub_form_3_2 = SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class)

        # Expected result, manually calculated
        manually_result = 0.20

        assert sub_form_3_2 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_invalid_cement_class_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        cement_class = "V"  # str

        with pytest.raises(ValueError):
            SubForm3Dot2CoefficientTypeOfCementS(cement_class=cement_class)
