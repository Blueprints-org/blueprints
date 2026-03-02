"""Testing formula 8.37 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2025.chapter_8_ultimate_limit_state.formula_8_37 import Form8Dot37Rho
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot37Rho:
    """Validation for formula 8.37 from EN 1993-1-1:2025, chapter 8, ultimate limit state."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 300.0
        v_c_rd = 500.0

        # Object to test
        formula = Form8Dot37Rho(v_ed=v_ed, v_c_rd=v_c_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.04  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100.0
        v_c_rd = 500.0

        # Object to test
        formula = Form8Dot37Rho(v_ed=v_ed, v_c_rd=v_c_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.0  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "v_c_rd"),
        [
            (-300.0, 500.0),  # v_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, v_ed: float, v_c_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot37Rho(v_ed=v_ed, v_c_rd=v_c_rd)

    @pytest.mark.parametrize(
        ("v_ed", "v_c_rd"),
        [
            (300.0, 0.0),  # v_c_rd is zero
            (300.0, -500.0),  # v_c_rd is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, v_ed: float, v_c_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot37Rho(v_ed=v_ed, v_c_rd=v_c_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho = \begin{cases} "
                r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{c,Rd} \\ "
                r"\left( \frac{2 \cdot V_{Ed}}{V_{c,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{c,Rd} "
                r"\end{cases} = \begin{cases} "
                r"0 & \text{if } 300.000 \leq 0.5 \cdot 500.000 \\ "
                r"\left( \frac{2 \cdot 300.000}{500.000} - 1 \right)^2 & \text{if } 300.000 > 0.5 \cdot 500.000 "
                r"\end{cases} = 0.040 \ -",
            ),
            (
                "complete_with_units",
                r"\rho = \begin{cases} "
                r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{c,Rd} \\ "
                r"\left( \frac{2 \cdot V_{Ed}}{V_{c,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{c,Rd} "
                r"\end{cases} = \begin{cases} "
                r"0 & \text{if } 300.000 \ N \leq 0.5 \cdot 500.000 \ N \\ "
                r"\left( \frac{2 \cdot 300.000 \ N}{500.000 \ N} - 1 \right)^2 & \text{if } 300.000 \ N > 0.5 \cdot 500.000 \ N "
                r"\end{cases} = 0.040 \ -",
            ),
            ("short", r"\rho = 0.040 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 300.0
        v_c_rd = 500.0

        # Object to test
        latex = Form8Dot37Rho(v_ed=v_ed, v_c_rd=v_c_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
