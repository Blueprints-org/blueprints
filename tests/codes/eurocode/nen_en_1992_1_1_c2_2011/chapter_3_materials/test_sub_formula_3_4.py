"""Testing sub-formula for 3.4 of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_3_materials.formula_3_4 import SubForm3Dot4CoefficientAgeConcreteAlpha


class TestSubForm3Dot4CoefficientAgeConcreteAlpha:
    """Validation for sub-formula 3.4 from NEN-EN 1992-1-1+C2:2011."""

    def test_t_between_0_and_28(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        t = 10  # days

        sub_form_3_4 = SubForm3Dot4CoefficientAgeConcreteAlpha(t=t)

        # Expected result, manually calculated
        manually_result = 1.0

        assert sub_form_3_4 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_t_lower_or_equal_to_0(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        t = 0  # days

        with pytest.raises(ValueError):
            SubForm3Dot4CoefficientAgeConcreteAlpha(t=t)

    def test_t_higher_then_28(self) -> None:
        """Test the evaluation of the result."""
        # Example value 1
        t = 50  # days

        sub_form_3_4 = SubForm3Dot4CoefficientAgeConcreteAlpha(t=t)

        # Expected result, manually calculated
        manually_result = 2 / 3

        assert sub_form_3_4 == pytest.approx(expected=manually_result, rel=1e-4)
