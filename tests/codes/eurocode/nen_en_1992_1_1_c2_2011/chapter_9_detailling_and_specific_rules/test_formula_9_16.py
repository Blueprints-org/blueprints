"""Testing formula 9.16 of NEN-EN 1992-1-1+C2:2011."""
import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_9_detailling_and_specific_rules.formula_9_16 import (
    Form9Dot16MinimumForceOnInternalBeamLine,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot16MinimumForceOnInternalBeamLine:
    """Validation for formula 9.16 from NEN-EN 1992-1-1+C2:2011."""

    def test_evaluation(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        q_3 = 20  # kN/m,
        l_1 = 4.5  # m,
        l_2 = 4  # m,
        q_4 = 70  # kN,
        form_9_16 = Form9Dot16MinimumForceOnInternalBeamLine(
            q_3=q_3,
            l_1=l_1,
            l_2=l_2,
            q_4=q_4,
        )

        # Expected result, manually calculated
        manually_calculated_result = 85

        assert form_9_16 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_lower_limit(self) -> None:
        """Test the evaluation of the result."""
        # Example values
        q_3 = 20  # kN/m,
        l_1 = 1.5  # m,
        l_2 = 2  # m,
        q_4 = 70  # kN,
        form_9_16 = Form9Dot16MinimumForceOnInternalBeamLine(
            q_3=q_3,
            l_1=l_1,
            l_2=l_2,
            q_4=q_4,
        )
        # Expected result, manually calculated
        manually_calculated_result = 70

        assert form_9_16 == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_negative_q_3_is_given(self) -> None:
        """Test the evaluation of the result."""
        q_3 = -20  # kN/m,
        l_1 = 1.5  # m,
        l_2 = 2  # m,
        q_4 = 70  # kN,

        with pytest.raises(NegativeValueError):
            Form9Dot16MinimumForceOnInternalBeamLine(
                q_3=q_3,
                l_1=l_1,
                l_2=l_2,
                q_4=q_4,
            )

    def test_raise_error_when_negative_l_1_is_given(self) -> None:
        """Test the evaluation of the result."""
        q_3 = 20  # kN/m,
        l_1 = -1.5  # m,
        l_2 = 2  # m,
        q_4 = 70  # kN,

        with pytest.raises(NegativeValueError):
            Form9Dot16MinimumForceOnInternalBeamLine(
                q_3=q_3,
                l_1=l_1,
                l_2=l_2,
                q_4=q_4,
            )

    def test_raise_error_when_negative_l_2_is_given(self) -> None:
        """Test the evaluation of the result."""
        q_3 = 20  # kN/m,
        l_1 = 1.5  # m,
        l_2 = -2  # m,
        q_4 = 70  # kN,

        with pytest.raises(NegativeValueError):
            Form9Dot16MinimumForceOnInternalBeamLine(
                q_3=q_3,
                l_1=l_1,
                l_2=l_2,
                q_4=q_4,
            )

    def test_raise_error_when_negative_q_4_is_given(self) -> None:
        """Test the evaluation of the result."""
        q_3 = 20  # kN/m,
        l_1 = 1.5  # m,
        l_2 = 2  # m,
        q_4 = -70  # kN,

        with pytest.raises(NegativeValueError):
            Form9Dot16MinimumForceOnInternalBeamLine(
                q_3=q_3,
                l_1=l_1,
                l_2=l_2,
                q_4=q_4,
            )
