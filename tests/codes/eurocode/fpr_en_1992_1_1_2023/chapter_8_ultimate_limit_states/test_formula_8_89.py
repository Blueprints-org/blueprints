"""Testing formula 8.89 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_89 import (
    Form8Dot89CheckMaximumPunchingShearResistance,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot89CheckMaximumPunchingShearResistance:
    """Validation for formula 8.89 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rd_max", "expected"),
        [
            (2.50, 3.20, True),  # the maximum punching shear resistance is not exceeded
            (3.20, 3.20, True),  # exactly on the boundary, which the standard includes
            (3.60, 3.20, False),  # the maximum punching shear resistance is exceeded
        ],
    )
    def test_evaluation(self, tau_ed: float, tau_rd_max: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot89CheckMaximumPunchingShearResistance(tau_ed=tau_ed, tau_rd_max=tau_rd_max)) is expected

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rd_max"),
        [
            (-2.50, 3.20),  # tau_ed is negative
            (2.50, -3.20),  # tau_rd_max is negative
            (2.50, 0.0),  # tau_rd_max is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_ed: float, tau_rd_max: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot89CheckMaximumPunchingShearResistance(tau_ed=tau_ed, tau_rd_max=tau_rd_max)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (2.50, "complete", r"CHECK \to \tau_{Ed} \leq \tau_{Rd,max} \to 2.500 \leq 3.200 \to OK"),
            (2.50, "complete_with_units", r"CHECK \to \tau_{Ed} \leq \tau_{Rd,max} \to 2.500 \ MPa \leq 3.200 \ MPa \to OK"),
            (2.50, "short", r"CHECK \to OK"),
            (3.60, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot89CheckMaximumPunchingShearResistance(tau_ed=tau_ed, tau_rd_max=3.20).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
