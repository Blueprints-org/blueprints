"""Testing formula 6.39 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_39 import Form6Dot39BetaCoefficient
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot39BetaCoefficient:
    """Validation for formula 6.39 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        k = 1.0
        m_ed = 100.0
        v_ed = 200.0
        u_1 = 300.0
        w_1 = 400.0

        # Object to test
        formula = Form6Dot39BetaCoefficient(k=k, m_ed=m_ed, v_ed=v_ed, u_1=u_1, w_1=w_1)

        # Expected result, manually calculated
        manually_calculated_result = 1.375  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("k", "m_ed", "v_ed", "u_1", "w_1"),
        [
            (-1.0, 100.0, 200.0, 300.0, 400.0),  # k is negative
            (1.0, -100.0, 200.0, 300.0, 400.0),  # m_ed is negative
            (1.0, 100.0, -200.0, 300.0, 400.0),  # v_ed is negative
            (1.0, 100.0, 200.0, -300.0, 400.0),  # u_1 is negative
            (1.0, 100.0, 200.0, 300.0, -400.0),  # w_1 is negative
            (1.0, 100.0, 0.0, 300.0, 400.0),  # v_ed is zero
            (1.0, 100.0, 200.0, 300.0, 0.0),  # w_1 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, k: float, m_ed: float, v_ed: float, u_1: float, w_1: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot39BetaCoefficient(k=k, m_ed=m_ed, v_ed=v_ed, u_1=u_1, w_1=w_1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta = 1 + k \cdot \frac{M_{Ed}}{V_{Ed}} \cdot \frac{u_1}{W_1} = "
                r"1 + 1.000 \cdot \frac{100.000}{200.000} \cdot \frac{300.000}{400.000} = 1.375 \ -",
            ),
            ("short", r"\beta = 1.375 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        k = 1.0
        m_ed = 100.0
        v_ed = 200.0
        u_1 = 300.0
        w_1 = 400.0

        # Object to test
        latex = Form6Dot39BetaCoefficient(k=k, m_ed=m_ed, v_ed=v_ed, u_1=u_1, w_1=w_1).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
