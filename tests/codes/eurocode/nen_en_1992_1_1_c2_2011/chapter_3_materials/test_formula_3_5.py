"""Testing formula 3.5 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_5 import Form3Dot5ApproximationVarianceElasticModulusOverTime


class TestForm3Dot5ApproximationVarianceElasticModulusOverTime:
    """Validation for formula 3.5 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = 2.9  # MPa
        form_3_5 = Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

        # Expected result, manually calculated
        manually_calculated_result = 2.592502

        assert form_3_5 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_f_cm_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cm_t = -2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = 2.9  # MPa

        with pytest.raises(ValueError):
            Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

    def test_raise_error_when_negative_f_cm_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = -3.4  # MPa
        e_cm = 2.9  # MPa

        with pytest.raises(ValueError):
            Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)

    def test_raise_error_when_negative_e_cm_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        f_cm_t = 2.34  # MPa
        f_cm = 3.4  # MPa
        e_cm = -2.9  # MPa

        with pytest.raises(ValueError):
            Form3Dot5ApproximationVarianceElasticModulusOverTime(f_cm_t=f_cm_t, f_cm=f_cm, e_cm=e_cm)
