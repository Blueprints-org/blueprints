"""Testing formula 5.32 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_32 import Form5Dot32EquivalentFirstOrderEndMoment
from blueprints.validations import NegativeValueError


class TestForm5Dot32EquivalentFirstOrderEndMoment:
    """Validation for formula 5.32 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_01 = 30.0
        m_02 = 50.0

        # Object to test
        formula = Form5Dot32EquivalentFirstOrderEndMoment(m_01=m_01, m_02=m_02)

        # Expected result, manually calculated
        manually_calculated_result = 42.0  # kNm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_01", "m_02"),
        [
            (50.0, 30.0),  # m_02 is smaller than m_01
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_01: float, m_02: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, ValueError)):
            Form5Dot32EquivalentFirstOrderEndMoment(m_01=m_01, m_02=m_02)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"M_{0e} = \max\left(0.6 \cdot M_{02} + 0.4 \cdot M_{01}; 0.4 \cdot M_{02}\right) "
                r"= \max\left(0.6 \cdot 50.000 + 0.4 \cdot 30.000; 0.4 \cdot 50.000\right) = 42.000 \ kNm",
            ),
            ("short", r"M_{0e} = 42.000 \ kNm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_01 = 30.0
        m_02 = 50.0

        # Object to test
        latex = Form5Dot32EquivalentFirstOrderEndMoment(m_01=m_01, m_02=m_02).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
