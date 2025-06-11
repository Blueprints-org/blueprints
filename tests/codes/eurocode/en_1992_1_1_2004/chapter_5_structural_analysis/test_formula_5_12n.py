"""Testing formula 5.12N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_12n import (
    Form5Dot12nRatioDistancePointZeroAndMaxMoment,
)
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot12nRatioDistancePointZeroAndMaxMoment:
    """Validation for formula 5.12N from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        m_sd = 100  # kNm
        v_sd = 10  # kN
        d = 0.3  # m

        # Object to test
        formula = Form5Dot12nRatioDistancePointZeroAndMaxMoment(m_sd=m_sd, v_sd=v_sd, d=d)

        # Expected result, manually calculated
        manually_calculated_result = 33.333  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("m_sd", "v_sd", "d"),
        [
            (-100, 10, 0.3),
            (100, -10, 0.3),
            (100, 10, -0.3),
            (0, 10, 0.3),
            (100, 0, 0.3),
            (100, 10, 0),
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, m_sd: float, v_sd: float, d: float) -> None:
        """Test negative values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot12nRatioDistancePointZeroAndMaxMoment(m_sd=m_sd, v_sd=v_sd, d=d)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"λ = \frac{M_{sd}}{V_{sd} \cdot d} = \frac{100.000}{10.000 \cdot 0.300} = 33.333",
            ),
            ("short", r"λ = 33.333"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        m_sd = 100
        v_sd = 10
        d = 0.3

        # Object to test
        latex = Form5Dot12nRatioDistancePointZeroAndMaxMoment(m_sd=m_sd, v_sd=v_sd, d=d).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
