"""Testing formula 8.79 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_79 import (
    Form8Dot79TorsionalShearStressInWall,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot79TorsionalShearStressInWall:
    """Validation for formula 8.79 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        t_ed = 90000000.0
        a_k = 200000.0
        t_eff_i = 120.0

        # Object to test
        formula = Form8Dot79TorsionalShearStressInWall(t_ed=t_ed, a_k=a_k, t_eff_i=t_eff_i)

        # Expected result, manually calculated: 90000000 / (2 * 200000 * 120) = 90000000 / 48000000
        manually_calculated_result = 1.875  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_zero_torsional_moment(self) -> None:
        """Tests that a section without torsion gives no torsional shear stress."""
        # Object to test
        formula = Form8Dot79TorsionalShearStressInWall(t_ed=0.0, a_k=200000.0, t_eff_i=120.0)

        # Expected result, manually calculated: 0 / (2 * 200000 * 120)
        manually_calculated_result = 0.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, abs=1e-9)

    @pytest.mark.parametrize(
        ("t_ed", "a_k", "t_eff_i"),
        [
            (-90000000.0, 200000.0, 120.0),  # t_ed is negative
            (90000000.0, -200000.0, 120.0),  # a_k is negative
            (90000000.0, 0.0, 120.0),  # a_k is zero
            (90000000.0, 200000.0, -120.0),  # t_eff_i is negative
            (90000000.0, 200000.0, 0.0),  # t_eff_i is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, t_ed: float, a_k: float, t_eff_i: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form8Dot79TorsionalShearStressInWall(t_ed=t_ed, a_k=a_k, t_eff_i=t_eff_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{t,i} = \frac{T_{Ed}}{2 \cdot A_k \cdot t_{eff,i}} = "
                    r"\frac{90000000.000}{2 \cdot 200000.000 \cdot 120.000} = 1.875 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{t,i} = \frac{T_{Ed}}{2 \cdot A_k \cdot t_{eff,i}} = "
                    r"\frac{90000000.000 \ Nmm}{2 \cdot 200000.000 \ mm^2 \cdot 120.000 \ mm} = 1.875 \ MPa"
                ),
            ),
            ("short", r"\tau_{t,i} = 1.875 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        t_ed = 90000000.0
        a_k = 200000.0
        t_eff_i = 120.0

        # Object to test
        latex = Form8Dot79TorsionalShearStressInWall(t_ed=t_ed, a_k=a_k, t_eff_i=t_eff_i).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
