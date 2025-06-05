"""Testing sub-formulas for 5.1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_1 import (
    SubForm5Dot1ReductionFactorLengthOrHeight,
    SubForm5Dot1ReductionFactorNumberOfMembers,
)
from blueprints.validations import LessOrEqualToZeroError


class TestSubForm5Dot1ReductionFactorLengthOrHeight:
    """Validation for sub-formula (αh) for 5.1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        length = 8  # m

        # Object to test
        sub_form_5_1 = SubForm5Dot1ReductionFactorLengthOrHeight(length=length)

        # Expected result, manually calculated
        manually_calculated_result = 0.7071

        assert sub_form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_l_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        length = -3.5

        with pytest.raises(LessOrEqualToZeroError):
            SubForm5Dot1ReductionFactorLengthOrHeight(length=length)

    def test_raise_error_when_l_is_zero(self) -> None:
        """Test a zero value."""
        # Example values
        length = 0

        with pytest.raises(LessOrEqualToZeroError):
            SubForm5Dot1ReductionFactorLengthOrHeight(length=length)

    def test_alpha_h_is_between_two_thirds_when_l_is_high(self) -> None:
        """Test if the result is 2/3 when l is high."""
        # Example values
        length = 100  # m

        # Object to test
        sub_form_5_1 = SubForm5Dot1ReductionFactorLengthOrHeight(length=length)

        assert sub_form_5_1 == pytest.approx(expected=2 / 3, rel=1e-4)

    def test_alpha_h_is_one_when_l_is_low(self) -> None:
        """Test if the result is 1 when l is low."""
        # Example values
        length = 0.1

        # Object to test
        sub_form_5_1 = SubForm5Dot1ReductionFactorLengthOrHeight(length=length)

        assert sub_form_5_1 == pytest.approx(expected=1, rel=1e-4)


class TestSubForm5Dot1ReductionFactorNumberOfMembers:
    """Validation for sub-formula (αm) for 5.1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        members = 5

        # Object to test
        sub_form_5_1 = SubForm5Dot1ReductionFactorNumberOfMembers(members=members)

        # Expected result, manually calculated
        manually_calculated_result = 0.774596

        assert sub_form_5_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_m_is_given(self) -> None:
        """Test a negative value."""
        # Example values
        members = -5

        with pytest.raises(LessOrEqualToZeroError):
            SubForm5Dot1ReductionFactorNumberOfMembers(members=members)

    def test_raise_error_when_m_is_zero(self) -> None:
        """Test a zero value."""
        # Example values
        members = 0

        with pytest.raises(LessOrEqualToZeroError):
            SubForm5Dot1ReductionFactorNumberOfMembers(members=members)
