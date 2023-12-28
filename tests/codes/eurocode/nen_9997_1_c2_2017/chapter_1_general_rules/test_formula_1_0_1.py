""""Test formula 1.0.1 from NEN 9997-1+C2:2017: Chapter 1: General rules."""
import pytest

from blueprints.codes.eurocode.nen_9997_1_c2_2017.chapter_1_general_rules.formula_1_0_1 import Form1Dot0Dot1EquivalentPilePointCenterline
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm1Dot0Dot1EquivalentPilePointCenterline:
    """Validation for formula 1.0.1 from NEN 9997-1+C2:2017."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # example values
        a = 0.3  # m
        b = 0.45  # m

        form_1_0_1 = Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b)

        # manually calculated result
        manually_calculated_result = 0.415188

        assert form_1_0_1 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_if_negative_b(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for b."""
        a = 0.3
        b = -0.45

        with pytest.raises(NegativeValueError):
            Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b)

    def test_raise_error_if_a_is_zero(self) -> None:
        """Test that a NegativeValueError is raised when 0 is passed for a."""
        a = 0
        b = 0.45

        with pytest.raises(LessOrEqualToZeroError):
            Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b)

    def test_raise_error_if_a_is_negative(self) -> None:
        """Test that a NegativeValueError is raised when a negative value is passed for a."""
        a = -0.3
        b = 0.45

        with pytest.raises(LessOrEqualToZeroError):
            Form1Dot0Dot1EquivalentPilePointCenterline(a=a, b=b)
