"""Testing formula 8.32 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_32 import Form8Dot32VplTRdChannelSection
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot32VplTRdChannelSection:
    """Validation for formula 8.32 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        tau_t_ed = 100.0
        f_y = 355.0
        gamma_m0 = 1.0
        tau_w_ed = 50.0
        v_pl_rd = 200000.0

        # Object to test
        formula = Form8Dot32VplTRdChannelSection(
            tau_t_ed=tau_t_ed,
            f_y=f_y,
            gamma_m0=gamma_m0,
            tau_w_ed=tau_w_ed,
            v_pl_rd=v_pl_rd,
        )

        # Expected result, manually calculated
        manually_calculated_result = 107373.685136  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_t_ed", "f_y", "gamma_m0", "tau_w_ed", "v_pl_rd"),
        [
            (-100.0, 355.0, 1.0, 50.0, 200000.0),  # tau_t_ed is negative
            (100.0, 355.0, 1.0, 50.0, -200000.0),  # v_pl_rd is negative
            (100.0, 355.0, 1.0, -50.0, 200000.0),  # tau_w_ed is negative
            (1e9, 355.0, 1.0, 50.0, 200000.0),  # square root becomes negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_t_ed: float, f_y: float, gamma_m0: float, tau_w_ed: float, v_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot32VplTRdChannelSection(
                tau_t_ed=tau_t_ed,
                f_y=f_y,
                gamma_m0=gamma_m0,
                tau_w_ed=tau_w_ed,
                v_pl_rd=v_pl_rd,
            )

    @pytest.mark.parametrize(
        ("tau_t_ed", "f_y", "gamma_m0", "tau_w_ed", "v_pl_rd"),
        [
            (100.0, 0.0, 1.0, 50.0, 200000.0),  # f_y is zero
            (100.0, -355.0, 1.0, 50.0, 200000.0),  # f_y is negative
            (100.0, 355.0, 0.0, 50.0, 200000.0),  # gamma_m0 is zero
            (100.0, 355.0, -1.0, 50.0, 200000.0),  # gamma_m0 is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(
        self, tau_t_ed: float, f_y: float, gamma_m0: float, tau_w_ed: float, v_pl_rd: float
    ) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot32VplTRdChannelSection(
                tau_t_ed=tau_t_ed,
                f_y=f_y,
                gamma_m0=gamma_m0,
                tau_w_ed=tau_w_ed,
                v_pl_rd=v_pl_rd,
            )

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{pl,T,Rd} = \left( \sqrt{1 - \frac{\tau_{t,Ed}}{1.25 \cdot \left( f_y / \sqrt{3} \right) / \gamma_{M0}}} - "
                r"\frac{\tau_{w,Ed}}{\left( f_y / \sqrt{3} \right) / \gamma_{M0}} \right) \cdot V_{pl,Rd} = "
                r"\left( \sqrt{1 - \frac{100.000}{1.25 \cdot \left( 355.000 / \sqrt{3} \right) / 1.000}} - "
                r"\frac{50.000}{\left( 355.000 / \sqrt{3} \right) / 1.000} \right) \cdot 200000.000 = 107373.685 \ N",
            ),
            ("short", r"V_{pl,T,Rd} = 107373.685 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_t_ed = 100.0
        f_y = 355.0
        gamma_m0 = 1.0
        tau_w_ed = 50.0
        v_pl_rd = 200000.0

        # Object to test
        latex = Form8Dot32VplTRdChannelSection(
            tau_t_ed=tau_t_ed,
            f_y=f_y,
            gamma_m0=gamma_m0,
            tau_w_ed=tau_w_ed,
            v_pl_rd=v_pl_rd,
        ).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
