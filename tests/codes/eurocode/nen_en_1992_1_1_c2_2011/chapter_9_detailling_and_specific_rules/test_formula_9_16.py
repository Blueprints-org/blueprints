"""Testing formula 9.16 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_9_detailling_and_specific_rules.formula_9_16 import (
    Form9Dot16MinimumForceOnInternalBeamLine,
)
from blueprints.validations import NegativeValueError


class TestForm9Dot16MinimumForceOnInternalBeamLine:
    """Validation for formula 9.16 from EN 1992-1-1:2004."""

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

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (r"F_{tie} = min(q_3 \cdot (l_1 + l_2) / 2, Q_4) = min(20.00 \cdot (4.50 + 4.00) / 2, 70.00) = 85.00"),
            ),
            ("short", r"F_{tie} = 85.00"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        q_3 = 20  # kN/m,
        l_1 = 4.5  # m,
        l_2 = 4  # m,
        q_4 = 70  # kN,

        # Object to test
        form_9_16_latex = Form9Dot16MinimumForceOnInternalBeamLine(
            q_3=q_3,
            l_1=l_1,
            l_2=l_2,
            q_4=q_4,
        ).latex()

        actual = {"complete": form_9_16_latex.complete, "short": form_9_16_latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
