"""Testing sub-formula 1 of 3.14 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import SubForm3Dot14Eta


class TestSub1Form3Dot14Eta:
    """Validation for sub-formula 1 of 3.14 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation_1(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        epsilon_c = 0.16  # -
        epsilon_c1 = 0.43  # -

        sub_1_form_3_14 = SubForm3Dot14Eta(epsilon_c=epsilon_c, epsilon_c1=epsilon_c1)

        # Expected result, manually calculated
        manually_calculated_result = 0.37209

        assert sub_1_form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_2(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        epsilon_c = 0.3  # -
        epsilon_c1 = 0.2  # -

        sub_1_form_3_14 = SubForm3Dot14Eta(epsilon_c=epsilon_c, epsilon_c1=epsilon_c1)

        # Expected result, manually calculated
        manually_calculated_result = 1.5

        assert sub_1_form_3_14 == pytest.approx(expected=manually_calculated_result, rel=1e-4)
