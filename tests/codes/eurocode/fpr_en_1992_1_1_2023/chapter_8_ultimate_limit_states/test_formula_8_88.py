"""Testing formula 8.88 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_88 import (
    Form8Dot88CheckPunchingShearReinforcementMayBeOmitted,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot88CheckPunchingShearReinforcementMayBeOmitted:
    """Validation for formula 8.88 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rd_c", "expected"),
        [
            (0.90, 1.10, True),  # punching shear reinforcement may be omitted
            (1.10, 1.10, True),  # exactly on the boundary, which the standard includes
            (1.40, 1.10, False),  # punching shear reinforcement is required
        ],
    )
    def test_evaluation(self, tau_ed: float, tau_rd_c: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot88CheckPunchingShearReinforcementMayBeOmitted(tau_ed=tau_ed, tau_rd_c=tau_rd_c)) is expected

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rd_c"),
        [
            (-0.90, 1.10),  # tau_ed is negative
            (0.90, -1.10),  # tau_rd_c is negative
            (0.90, 0.0),  # tau_rd_c is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_ed: float, tau_rd_c: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot88CheckPunchingShearReinforcementMayBeOmitted(tau_ed=tau_ed, tau_rd_c=tau_rd_c)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (0.90, "complete", r"CHECK \to \tau_{Ed} \leq \tau_{Rd,c} \to 0.900 \leq 1.100 \to OK"),
            (0.90, "complete_with_units", r"CHECK \to \tau_{Ed} \leq \tau_{Rd,c} \to 0.900 \ MPa \leq 1.100 \ MPa \to OK"),
            (0.90, "short", r"CHECK \to OK"),
            (1.40, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot88CheckPunchingShearReinforcementMayBeOmitted(tau_ed=tau_ed, tau_rd_c=1.10).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
