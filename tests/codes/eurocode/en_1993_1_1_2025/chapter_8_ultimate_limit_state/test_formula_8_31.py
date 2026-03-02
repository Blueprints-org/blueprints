"""Testing formula 8.31 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_31 import Form8Dot31VplTRdIOrHSection
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot31VplTRdIOrHSection:
    """Validation for formula 8.31 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        tau_t_ed = 50.0
        f_y = 355.0
        gamma_m0 = 1.0
        v_pl_rd = 100000.0

        # Object to test
        formula = Form8Dot31VplTRdIOrHSection(tau_t_ed=tau_t_ed, f_y=f_y, gamma_m0=gamma_m0, v_pl_rd=v_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 89712.8388597  # N

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_t_ed", "v_pl_rd"),
        [
            (-50.0, 100000.0),  # tau_t_ed is negative
            (50.0, -100000.0),  # v_pl_rd is negative
            (1e9, 100000.0),  # square root becomes negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, tau_t_ed: float, v_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot31VplTRdIOrHSection(tau_t_ed=tau_t_ed, f_y=355.0, gamma_m0=1.0, v_pl_rd=v_pl_rd)

    @pytest.mark.parametrize(
        ("gamma_m0", "f_y"),
        [
            (0.0, 355.0),  # gamma_m0 is zero
            (-1.0, 355.0),  # gamma_m0 is negative
            (1.0, 0.0),  # f_y is zero
            (1.0, -355.0),  # f_y is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, gamma_m0: float, f_y: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot31VplTRdIOrHSection(tau_t_ed=10.0, f_y=f_y, gamma_m0=gamma_m0, v_pl_rd=100000.0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{pl,T,Rd} = \sqrt{1 - \frac{\tau_{t,Ed}}{1.25 \cdot \left( f_y / \sqrt{3} \right) / \gamma_{M0}}} \cdot V_{pl,Rd} = "
                r"\sqrt{1 - \frac{50.000}{1.25 \cdot \left( 355.000 / \sqrt{3} \right) / 1.000}} \cdot 100000.000 = 89712.839 \ N",
            ),
            ("short", r"V_{pl,T,Rd} = 89712.839 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_t_ed = 50.0
        f_y = 355.0
        gamma_m0 = 1.0
        v_pl_rd = 100000.0

        # Object to test
        formula = Form8Dot31VplTRdIOrHSection(tau_t_ed=tau_t_ed, f_y=f_y, gamma_m0=gamma_m0, v_pl_rd=v_pl_rd)
        latex = formula.latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
