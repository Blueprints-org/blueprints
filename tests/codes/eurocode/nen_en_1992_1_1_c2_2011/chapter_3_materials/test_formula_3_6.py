"""Testing formula 3.6 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot6CreepDeformationOfConcrete


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

    def test_raise_error_when_negative_phi_inf_t0_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = -0.34  # -
        sigma_c = 0.75  # MPa
        e_c = 2.45  # MPa

        with pytest.raises(ValueError):
            Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

    def test_raise_error_when_negative_sigma_c_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = -0.75  # MPa
        e_c = 2.45  # MPa

        with pytest.raises(ValueError):
            Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)

    def test_raise_error_when_negative_e_c_is_given(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        phi_inf_t0 = 0.34  # -
        sigma_c = 0.75  # MPa
        e_c = -2.45  # MPa

        with pytest.raises(ValueError):
            Form3Dot6CreepDeformationOfConcrete(phi_inf_t0=phi_inf_t0, sigma_c=sigma_c, e_c=e_c)
