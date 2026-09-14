"""Testing formula 8.87 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_87 import (
    Form8Dot87CheckDetailedPunchingVerificationMayBeOmitted,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot87CheckDetailedPunchingVerificationMayBeOmitted:
    """Validation for formula 8.87 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rdc_min", "expected"),
        [
            (0.45, 0.60, True),  # the detailed verification may be omitted
            (0.60, 0.60, True),  # exactly on the boundary, which the standard includes
            (0.75, 0.60, False),  # the detailed verification is required
        ],
    )
    def test_evaluation(self, tau_ed: float, tau_rdc_min: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot87CheckDetailedPunchingVerificationMayBeOmitted(tau_ed=tau_ed, tau_rdc_min=tau_rdc_min)) is expected

    @pytest.mark.parametrize(
        ("tau_ed", "tau_rdc_min"),
        [
            (-0.45, 0.60),  # tau_ed is negative
            (0.45, -0.60),  # tau_rdc_min is negative
            (0.45, 0.0),  # tau_rdc_min is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_ed: float, tau_rdc_min: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot87CheckDetailedPunchingVerificationMayBeOmitted(tau_ed=tau_ed, tau_rdc_min=tau_rdc_min)

    @pytest.mark.parametrize(
        ("tau_ed", "representation", "expected"),
        [
            (0.45, "complete", r"CHECK \to \tau_{Ed} \leq \tau_{Rdc,min} \to 0.450 \leq 0.600 \to OK"),
            (0.45, "complete_with_units", r"CHECK \to \tau_{Ed} \leq \tau_{Rdc,min} \to 0.450 \ MPa \leq 0.600 \ MPa \to OK"),
            (0.45, "short", r"CHECK \to OK"),
            (0.75, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_ed: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot87CheckDetailedPunchingVerificationMayBeOmitted(tau_ed=tau_ed, tau_rdc_min=0.60).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
