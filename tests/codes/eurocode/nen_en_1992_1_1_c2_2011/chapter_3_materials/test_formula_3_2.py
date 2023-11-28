"""Testing formula 3.2 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials import Form3Dot2CoefficientDependentOfConcreteAge

# pylint: disable=arguments-differ


class TestForm3Dot2CoefficientDependentOfConcreteAge:
    """Validation for formula 3.2 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        s = 0.25  # -
        t = 10  # days
        form_3_2 = Form3Dot2CoefficientDependentOfConcreteAge(s=s, t=t)

        # Expected result, manually calculated
        manually_calculated_result = 0.84507490

        assert form_3_2 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_changing_value_after_initialization(self) -> None:
        """Test that an error is raised when changing a value after initialization."""
        # example values
        s = 1  # -
        t = 10  # MPa
        form_3_2 = Form3Dot2CoefficientDependentOfConcreteAge(s=s, t=t)

        with pytest.raises(AttributeError):
            form_3_2.s = 2
