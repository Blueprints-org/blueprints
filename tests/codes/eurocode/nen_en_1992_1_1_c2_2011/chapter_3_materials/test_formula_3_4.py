"""Testing formula 3.4 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot4DevelopmentTensileStrength

# pylint: disable=arguments-differ


class TestForm3Dot4DevelopmentTensileStrength:
    """Validation for formula 3.4 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        beta_cc_t = 0.32  # -
        alpha = 2 / 3  # -
        f_ctm = 3.45  # MPa
        form_3_4 = Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

        # Expected result, manually calculated
        manually_calculated_result = 1.614058

        assert form_3_4 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_alpha_is_unequal_to_1_or_2d3(self) -> None:
        """Test that an error is raised when alpha is unequal to 1 or 2/3."""
        # Example values
        beta_cc_t = 0.32  # -
        alpha = 1 / 3  # - -> unequal to 1 or 2/3
        f_ctm = 3.45

        with pytest.raises(ValueError):
            Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

    def test_raise_error_when_changing_value_after_initialization(self) -> None:
        """Test that an error is raised when changing a value after initialization."""
        # example values
        beta_cc_t = 0.32  # -
        alpha = 2 / 3
        f_ctm = 3.45
        form_3_4 = Form3Dot4DevelopmentTensileStrength(beta_cc_t=beta_cc_t, alpha=alpha, f_ctm=f_ctm)

        with pytest.raises(AttributeError):
            form_3_4.f_ctm = 2
