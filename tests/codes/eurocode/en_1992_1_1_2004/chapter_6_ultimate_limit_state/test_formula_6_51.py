"""Testing formula 6.51 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_51 import (
    Form6Dot51AppliedPunchingShearStressEccentricLoading,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot51AppliedPunchingShearStressEccentricLoading:
    """Validation for formula 6.51 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed_red = 10000.0
        u = 200.0
        d = 300.0
        k = 1.5
        m_ed = 400.0
        w = 500.0

        # Object to test
        formula = Form6Dot51AppliedPunchingShearStressEccentricLoading(v_ed_red=v_ed_red, u=u, d=d, k=k, m_ed=m_ed, w=w)

        # Expected result, manually calculated
        manually_calculated_result = 0.17066666666  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed_red", "u", "d", "k", "m_ed", "w"),
        [
            (-10000.0, 200.0, 300.0, 1.5, 400.0, 500.0),  # v_ed_red is negative
            (10000.0, -200.0, 300.0, 1.5, 400.0, 500.0),  # u is negative
            (10000.0, 200.0, -300.0, 1.5, 400.0, 500.0),  # d is negative
            (10000.0, 200.0, 300.0, -1.5, 400.0, 500.0),  # k is negative
            (10000.0, 200.0, 300.0, 1.5, -400.0, 500.0),  # m_ed is negative
            (10000.0, 200.0, 300.0, 1.5, 400.0, -500.0),  # w is negative
            (0.0, 200.0, 300.0, 1.5, 400.0, 500.0),  # v_ed_red is zero
            (10000.0, 0.0, 300.0, 1.5, 400.0, 500.0),  # u is zero
            (10000.0, 200.0, 0.0, 1.5, 400.0, 500.0),  # d is zero
            (10000.0, 200.0, 300.0, 1.5, 400.0, 0.0),  # w is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, v_ed_red: float, u: float, d: float, k: float, m_ed: float, w: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot51AppliedPunchingShearStressEccentricLoading(v_ed_red=v_ed_red, u=u, d=d, k=k, m_ed=m_ed, w=w)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"v_{Ed} = \frac{V_{Ed,red}}{u \cdot d} \cdot \left(1 + k \cdot \frac{M_{Ed} \cdot u}{V_{Ed,red} \cdot W}\right) = "
                r"\frac{10000.000}{200.000 \cdot 300.000} \cdot \left(1 + 1.500 \cdot \frac{400.000 \cdot 200.000}{10000.000 \cdot 500.000}"
                r"\right) = 0.171 \ MPa",
            ),
            ("short", r"v_{Ed} = 0.171 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed_red = 10000.0
        u = 200.0
        d = 300.0
        k = 1.5
        m_ed = 400.0
        w = 500.0

        # Object to test
        latex = Form6Dot51AppliedPunchingShearStressEccentricLoading(v_ed_red=v_ed_red, u=u, d=d, k=k, m_ed=m_ed, w=w).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
