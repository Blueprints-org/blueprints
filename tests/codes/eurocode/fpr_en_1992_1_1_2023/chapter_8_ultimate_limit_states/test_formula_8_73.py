"""Testing formula 8.73 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_73 import Form8Dot73CheckShearStressAtInterface
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot73CheckShearStressAtInterface:
    """Validation for formula 8.73 from FprEN 1992-1-1:2023."""

    @pytest.mark.parametrize(
        ("tau_edi", "tau_rdi", "expected"),
        [
            (0.8, 1.2, True),  # the interface resists the shear stress
            (1.2, 1.2, True),  # exactly on the boundary, which the standard includes
            (1.5, 1.2, False),  # the interface does not resist the shear stress
        ],
    )
    def test_evaluation(self, tau_edi: float, tau_rdi: float, expected: bool) -> None:
        """Tests the evaluation of the result."""
        assert bool(Form8Dot73CheckShearStressAtInterface(tau_edi=tau_edi, tau_rdi=tau_rdi)) is expected

    @pytest.mark.parametrize(
        ("tau_edi", "tau_rdi"),
        [
            (-0.8, 1.2),  # tau_edi is negative
            (0.8, -1.2),  # tau_rdi is negative
            (0.8, 0.0),  # tau_rdi is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_edi: float, tau_rdi: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot73CheckShearStressAtInterface(tau_edi=tau_edi, tau_rdi=tau_rdi)

    @pytest.mark.parametrize(
        ("tau_edi", "representation", "expected"),
        [
            (0.8, "complete", r"CHECK \to \tau_{Edi} \leq \tau_{Rdi} \to 0.800 \leq 1.200 \to OK"),
            (0.8, "complete_with_units", r"CHECK \to \tau_{Edi} \leq \tau_{Rdi} \to 0.800 \ MPa \leq 1.200 \ MPa \to OK"),
            (0.8, "short", r"CHECK \to OK"),
            (1.5, "short", r"CHECK \to \text{Not OK}"),
        ],
    )
    def test_latex(self, tau_edi: float, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot73CheckShearStressAtInterface(tau_edi=tau_edi, tau_rdi=1.2).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
