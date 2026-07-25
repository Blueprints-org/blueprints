"""Testing formula 8.30 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_30 import Form8Dot30EffectiveShearSpan
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot30EffectiveShearSpan:
    """Validation for formula 8.30 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result when the moment to shear ratio governs."""
        # Example values
        m_ed = 200000000.0
        v_ed = 150000.0
        d = 500.0

        # Object to test
        formula = Form8Dot30EffectiveShearSpan(m_ed=m_ed, v_ed=v_ed, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 1333.333333  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_when_the_effective_depth_governs(self) -> None:
        """Tests the evaluation of the result when the lower bound governs."""
        # Example values, with a moment to shear ratio of 333.333 mm, below the effective depth
        formula = Form8Dot30EffectiveShearSpan(m_ed=50000000.0, v_ed=150000.0, d=500.0)

        # Expected result, manually calculated
        manually_calculated_result = 500.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_ed", "v_ed"),
        [
            (-200000000.0, 150000.0),  # negative moment
            (200000000.0, -150000.0),  # negative shear force
            (-200000000.0, -150000.0),  # both negative
        ],
    )
    def test_evaluation_is_insensitive_to_signs(self, m_ed: float, v_ed: float) -> None:
        """Tests that the absolute value bars printed in the standard make the result sign insensitive."""
        formula = Form8Dot30EffectiveShearSpan(m_ed=m_ed, v_ed=v_ed, d=500.0)

        assert formula == pytest.approx(expected=1333.333333, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_ed", "v_ed", "d"),
        [
            (200000000.0, 0.0, 500.0),  # v_ed is zero
            (200000000.0, 150000.0, -500.0),  # d is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, m_ed: float, v_ed: float, d: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot30EffectiveShearSpan(m_ed=m_ed, v_ed=v_ed, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"a_{cs} = \max\left(\left|\frac{M_{Ed}}{V_{Ed}}\right|, d\right) = "
                r"\max\left(\left|\frac{200000000.000}{150000.000}\right|, 500.000\right) = 1333.333 \ mm",
            ),
            (
                "complete_with_units",
                r"a_{cs} = \max\left(\left|\frac{M_{Ed}}{V_{Ed}}\right|, d\right) = "
                r"\max\left(\left|\frac{200000000.000 \ Nmm}{150000.000 \ N}\right|, 500.000 \ mm\right) = 1333.333 \ mm",
            ),
            ("short", r"a_{cs} = 1333.333 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_ed = 200000000.0
        v_ed = 150000.0
        d = 500.0

        # Object to test
        latex = Form8Dot30EffectiveShearSpan(m_ed=m_ed, v_ed=v_ed, d=d).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
