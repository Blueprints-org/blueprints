"""Testing sub-formulas for 8.2 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_2 import (
    SubForm8Dot2CoefficientQualityOfBond,
)


class TestSubForm8Dot2CoefficientQualityOfBond:
    """Validation for sub-formula 8.2 from EN 1992-1-1:2004."""

    def test_evaluation_good(self) -> None:
        """Test the evaluation of the result."""
        bond_quality = "good"  # str
        sub_form_8_2_1 = SubForm8Dot2CoefficientQualityOfBond(bond_quality=bond_quality)
        # Expected result, manually calculated
        manually_result = 1
        assert sub_form_8_2_1 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_evaluation_other(self) -> None:
        """Test the evaluation of the result."""
        bond_quality = "other"  # str
        sub_form_8_2_2 = SubForm8Dot2CoefficientQualityOfBond(bond_quality=bond_quality)
        # Expected result, manually calculated
        manually_result = 0.7
        assert sub_form_8_2_2 == pytest.approx(expected=manually_result, rel=1e-4)

    def test_raise_error_when_invalid_bond_quality_is_given(self) -> None:
        """Test an invalid bond quality."""
        # Example values
        bond_quality = "military_grade"  # str

        with pytest.raises(ValueError):
            SubForm8Dot2CoefficientQualityOfBond(bond_quality=bond_quality)
