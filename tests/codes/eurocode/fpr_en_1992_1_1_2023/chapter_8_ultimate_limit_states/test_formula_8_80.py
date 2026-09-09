"""Testing formula 8.80 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_80 import (
    Form8Dot80ShearForceInWallDueToTorsion,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot80ShearForceInWallDueToTorsion:
    """Validation for formula 8.80 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        tau_t_i = 1.875
        t_eff_i = 120.0
        z_i = 400.0

        # Object to test
        formula = Form8Dot80ShearForceInWallDueToTorsion(tau_t_i=tau_t_i, t_eff_i=t_eff_i, z_i=z_i)

        # Expected result, manually calculated: 1.875 * 120 * 400 = 225 * 400
        manually_calculated_result = 90000.0  # N

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("tau_t_i", "t_eff_i", "z_i"),
        [
            (-1.875, 120.0, 400.0),  # tau_t_i is negative
            (1.875, -120.0, 400.0),  # t_eff_i is negative
            (1.875, 120.0, -400.0),  # z_i is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, tau_t_i: float, t_eff_i: float, z_i: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot80ShearForceInWallDueToTorsion(tau_t_i=tau_t_i, t_eff_i=t_eff_i, z_i=z_i)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"V_{Ed,i} = \tau_{t,i} \cdot t_{eff,i} \cdot z_i = 1.875 \cdot 120.000 \cdot 400.000 = 90000.000 \ N",
            ),
            (
                "complete_with_units",
                (
                    r"V_{Ed,i} = \tau_{t,i} \cdot t_{eff,i} \cdot z_i = "
                    r"1.875 \ MPa \cdot 120.000 \ mm \cdot 400.000 \ mm = 90000.000 \ N"
                ),
            ),
            ("short", r"V_{Ed,i} = 90000.000 \ N"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        tau_t_i = 1.875
        t_eff_i = 120.0
        z_i = 400.0

        # Object to test
        latex = Form8Dot80ShearForceInWallDueToTorsion(tau_t_i=tau_t_i, t_eff_i=t_eff_i, z_i=z_i).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
