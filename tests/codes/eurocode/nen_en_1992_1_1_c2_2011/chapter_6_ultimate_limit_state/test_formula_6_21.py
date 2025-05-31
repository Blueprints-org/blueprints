"""Testing formula 6.21 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_21 import Form6Dot21CheckTransverseReinforcement
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot21CheckTransverseReinforcement:
    """Validation for formula 6.21 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_sf = 100.0
        f_yd = 500.0
        s_f = 200.0
        v_ed = 2.0
        h_f = 300.0
        theta_f = 45.0

        # Object to test
        formula = Form6Dot21CheckTransverseReinforcement(a_sf=a_sf, f_yd=f_yd, s_f=s_f, v_ed=v_ed, h_f=h_f, theta_f=theta_f)

        # Expected result, manually calculated
        expected_result = False

        assert formula == expected_result

    @pytest.mark.parametrize(
        ("a_sf", "f_yd", "s_f", "v_ed", "h_f", "theta_f"),
        [
            (-100.0, 500.0, 200.0, 2.0, 300.0, 45.0),  # a_sf is negative
            (100.0, -500.0, 200.0, 2.0, 300.0, 45.0),  # f_yd is negative
            (100.0, 500.0, -200.0, 2.0, 300.0, 45.0),  # s_f is negative
            (100.0, 500.0, 200.0, -2.0, 300.0, 45.0),  # v_ed is negative
            (100.0, 500.0, 200.0, 2.0, -300.0, 45.0),  # h_f is negative
            (100.0, 500.0, 200.0, 2.0, 300.0, -45.0),  # theta_f is negative
            (100.0, 500.0, 0.0, 2.0, 300.0, 45.0),  # s_f is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_sf: float, f_yd: float, s_f: float, v_ed: float, h_f: float, theta_f: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot21CheckTransverseReinforcement(a_sf=a_sf, f_yd=f_yd, s_f=s_f, v_ed=v_ed, h_f=h_f, theta_f=theta_f)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"CHECK \to \left( \frac{A_{sf} \cdot f_{yd}}{s_{f}} \geq \frac{v_{Ed} \cdot h_{f}}{\cot(\theta_{f})} \right) \to"
                r" \left( \frac{100.000 \cdot 500.000}{200.000} \geq \frac{2.000 \cdot 300.000}{\cot(45.000)} \right) \to \text{Not OK}",
            ),
            ("short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_sf = 100.0
        f_yd = 500.0
        s_f = 200.0
        v_ed = 2.0
        h_f = 300.0
        theta_f = 45.0

        # Object to test
        latex = Form6Dot21CheckTransverseReinforcement(a_sf=a_sf, f_yd=f_yd, s_f=s_f, v_ed=v_ed, h_f=h_f, theta_f=theta_f).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
