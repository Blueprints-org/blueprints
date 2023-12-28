"""Testing formula 3.10 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_10 import Form3Dot10CoefficientAgeConcreteDryingShrinkage


class TestForm3Dot10CoefficientAgeConcreteDryingShrinkage:
    """Validation for formula 3.10 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        t = 10  # -
        t_s = 2  # -
        h_0 = 200  # -
        form_3_10 = Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

        # Expected result, manually calculated
        manually_calculated_result = 0.06604088

        assert form_3_10 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_t_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        t = -10  # -
        t_s = 2  # -
        h_0 = 200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    def test_raise_error_when_negative_t_s_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        t = 10  # -
        t_s = -2  # -
        h_0 = 200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    def test_raise_error_when_negative_h_0_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        t = 10  # -
        t_s = 2  # -
        h_0 = -200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)

    def test_raise_error_when_t_is_smaller_than_t_s(self) -> None:
        """Test a comparison."""
        # Example values
        t = 10  # -
        t_s = 12  # -
        h_0 = 200  # -

        with pytest.raises(ValueError):
            Form3Dot10CoefficientAgeConcreteDryingShrinkage(t=t, t_s=t_s, h_0=h_0)
