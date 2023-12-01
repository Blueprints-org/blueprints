"""Testing formula 3.1 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_1 import Form3Dot1EstimationConcreteCompressiveStrength


class TestForm3Dot1EstimationConcreteCompressiveStrength:
    """Validation for formula 3.1 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 1  # -
        f_cm = 10  # MPa
        form_3_1 = Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm)

        # Expected result, manually calculated
        manually_calculated_result = 10

        assert form_3_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_beta_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = -1  # -
        f_cm = 10  # MPa

        with pytest.raises(ValueError):
            Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm)

    def test_raise_error_when_negative_f_cm_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 1  # -
        f_cm = -10  # MPa

        with pytest.raises(ValueError):
            Form3Dot1EstimationConcreteCompressiveStrength(beta_cc_t=beta_cc_t, f_cm=f_cm)
