"""Testing formula 3.6 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot6CreepDeformationOfConcrete

# pylint: disable=arguments-differ


class TestForm3Dot6CreepDeformationOfConcrete:
    """Validation for formula 3.6 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = 0.75  # MPa
        e_c = 2.45  # MPa
        form_3_6 = Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

        # Expected result, manually calculated
        manually_calculated_result = 0.1040816

        assert form_3_6 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_changing_value_after_initialization(self) -> None:
        """Test that an error is raised when changing a value after initialization."""
        # example values
        phi_inf_t0 = 0.34  # -
        sigma_c = 0.75  # MPa
        e_c = 2.45  # MPa
        form_3_6 = Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

        with pytest.raises(AttributeError):
            form_3_6.sigma_c = 2
