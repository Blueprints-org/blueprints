"""Testing formula 9.15 of NEN-EN 1992-1-1+C2:2011."""
# pylint: disable=arguments-differ
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_15 import (
    Form9Dot15MinimumResistancePeripheralTie,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot15MinimumResistancePeripheralTie:
    """Validation for formula 9.15 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_i = 10  # m
        q_1 = 10  # kN/m
        q_2 = 70  # kN
        form_9_15 = Form9Dot15MinimumResistancePeripheralTie(l_i=l_i, q_1=q_1, q_2=q_2)

        # Expected result, manually calculated
        manually_calculated_result = 100

        assert form_9_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_lower_limit(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        l_i = 2  # m
        q_1 = 10  # kN/m
        q_2 = 70  # kN
        form_9_15 = Form9Dot15MinimumResistancePeripheralTie(l_i=l_i, q_1=q_1, q_2=q_2)

        # Expected result, manually calculated
        manually_calculated_result = 70

        assert form_9_15 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_l_i_is_given(self) -> None:
        """Test the evaluation of the result."""
        l_i = -10  # m
        q_1 = 10  # kN/m
        q_2 = 70  # kN

        with pytest.raises(NegativeValueError):
            Form9Dot15MinimumResistancePeripheralTie(l_i=l_i, q_1=q_1, q_2=q_2)

    def test_raise_error_when_negative_q_1_is_given(self) -> None:
        """Test the evaluation of the result."""
        l_i = 10  # m
        q_1 = -10  # kN/m
        q_2 = 70  # kN

        with pytest.raises(NegativeValueError):
            Form9Dot15MinimumResistancePeripheralTie(l_i=l_i, q_1=q_1, q_2=q_2)

    def test_raise_error_when_negative_q_2_is_given(self) -> None:
        """Test the evaluation of the result."""
        l_i = 10  # m
        q_1 = 10  # kN/m
        q_2 = -70  # kN

        with pytest.raises(NegativeValueError):
            Form9Dot15MinimumResistancePeripheralTie(l_i=l_i, q_1=q_1, q_2=q_2)
