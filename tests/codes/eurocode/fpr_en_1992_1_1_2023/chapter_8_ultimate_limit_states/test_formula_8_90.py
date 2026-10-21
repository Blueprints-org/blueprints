"""Testing formula 8.90 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_90 import (
    Form8Dot90CheckPunchingShearResistanceWithReinforcement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot90CheckPunchingShearResistanceWithReinforcement:
    """Validation for formula 8.90 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rd_cs", "expected"),
        [
            (2.50, 2.80, True),  # the provided punching shear reinforcement is sufficient
            (2.80, 2.80, True),  # exactly on the boundary, which the standard includes
            (3.10, 2.80, False),  # the provided punching shear reinforcement is not sufficient
        ],
    )
    def test_evaluation(self, tau_ed: float, tau_rd_cs: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot90CheckPunchingShearResistanceWithReinforcement(tau_ed=tau_ed, tau_rd_cs=tau_rd_cs)) is expected

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rd_cs"),
        [
            (-2.50, 2.80),  # tau_ed is negative
            (2.50, -2.80),  # tau_rd_cs is negative
            (2.50, 0.0),  # tau_rd_cs is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_ed: float, tau_rd_cs: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot90CheckPunchingShearResistanceWithReinforcement(tau_ed=tau_ed, tau_rd_cs=tau_rd_cs)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (2.50, "complete", r"CHECK \to \tau_{Ed} \leq \tau_{Rd,cs} \to 2.500 \leq 2.800 \to OK"),
            (2.50, "complete_with_units", r"CHECK \to \tau_{Ed} \leq \tau_{Rd,cs} \to 2.500 \ MPa \leq 2.800 \ MPa \to OK"),
            (2.50, "short", r"CHECK \to OK"),
            (3.10, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot90CheckPunchingShearResistanceWithReinforcement(tau_ed=tau_ed, tau_rd_cs=2.80).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
