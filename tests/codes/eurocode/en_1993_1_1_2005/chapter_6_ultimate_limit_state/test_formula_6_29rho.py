"""Testing formula 6.29rho of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_29rho import (
    Form6Dot29Rho,
    Form6Dot29RhoWithTorsion,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot29Rho:
    """Validation for formula 6.29rho from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 300.0
        v_pl_rd = 500.0

        # Object to test
        formula = Form6Dot29Rho(v_ed=v_ed, v_pl_rd=v_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.04  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100.0
        v_pl_rd = 500.0

        # Object to test
        formula = Form6Dot29Rho(v_ed=v_ed, v_pl_rd=v_pl_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.0  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_rd"),
        [
            (-300.0, 500.0),  # v_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, v_ed: float, v_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot29Rho(v_ed=v_ed, v_pl_rd=v_pl_rd)

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_rd"),
        [
            (300.0, 0.0),  # v_pl_rd is zero
            (300.0, -500.0),  # v_pl_rd is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, v_ed: float, v_pl_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot29Rho(v_ed=v_ed, v_pl_rd=v_pl_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho = \begin{cases} "
                r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{pl,Rd} \\ "
                r"\left( \frac{2 \cdot V_{Ed}}{V_{pl,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{pl,Rd} "
                r"\end{cases} = \begin{cases} "
                r"0 & \text{if } 300.000 \leq 0.5 \cdot 500.000 \\ "
                r"\left( \frac{2 \cdot 300.000}{500.000} - 1 \right)^2 & \text{if } 300.000 > 0.5 \cdot 500.000 "
                r"\end{cases} = 0.040 \ -",
            ),
            (
                "complete_with_units",
                r"\rho = \begin{cases} "
                r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{pl,Rd} \\ "
                r"\left( \frac{2 \cdot V_{Ed}}{V_{pl,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{pl,Rd} "
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
        v_pl_rd = 500.0

        # Object to test
        latex = Form6Dot29Rho(v_ed=v_ed, v_pl_rd=v_pl_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm6Dot29RhoWithTorsion:
    """Validation for formula 6.29rho with torsion from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 600.0
        v_pl_t_rd = 1000.0

        # Object to test
        formula = Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.04  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation2(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        v_ed = 100.0
        v_pl_t_rd = 1000.0

        # Object to test
        formula = Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

        # Expected result, manually calculated
        manually_calculated_result = 0.00  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_t_rd"),
        [
            (-600.0, 1000.0),  # v_ed is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, v_ed: float, v_pl_t_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

    @pytest.mark.parametrize(
        ("v_ed", "v_pl_t_rd"),
        [
            (600.0, 0.0),  # v_pl_t_rd is zero
            (600.0, -1000.0),  # v_pl_t_rd is negative
        ],
    )
    def test_raise_error_when_less_or_equal_to_zero_values_are_given(self, v_ed: float, v_pl_t_rd: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\rho = \begin{cases} "
                r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{pl,T,Rd} \\ "
                r"\left( \frac{2 \cdot V_{Ed}}{V_{pl,T,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{pl,T,Rd} "
                r"\end{cases} = \begin{cases} "
                r"0 & \text{if } 600.000 \leq 0.5 \cdot 1000.000 \\ "
                r"\left( \frac{2 \cdot 600.000}{1000.000} - 1 \right)^2 & \text{if } 600.000 > 0.5 \cdot 1000.000 "
                r"\end{cases} = 0.040 \ -",
            ),
            (
                "complete_with_units",
                r"\rho = \begin{cases} "
                r"0 & \text{if } V_{Ed} \leq 0.5 \cdot V_{pl,T,Rd} \\ "
                r"\left( \frac{2 \cdot V_{Ed}}{V_{pl,T,Rd}} - 1 \right)^2 & \text{if } V_{Ed} > 0.5 \cdot V_{pl,T,Rd} "
                r"\end{cases} = \begin{cases} "
                r"0 & \text{if } 600.000 \ N \leq 0.5 \cdot 1000.000 \ N \\ "
                r"\left( \frac{2 \cdot 600.000 \ N}{1000.000 \ N} - 1 \right)^2 & \text{if } 600.000 \ N > 0.5 \cdot 1000.000 \ N "
                r"\end{cases} = 0.040 \ -",
            ),
            ("short", r"\rho = 0.040 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        v_ed = 600.0
        v_pl_t_rd = 1000.0

        # Object to test
        latex = Form6Dot29RhoWithTorsion(v_ed=v_ed, v_pl_t_rd=v_pl_t_rd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
