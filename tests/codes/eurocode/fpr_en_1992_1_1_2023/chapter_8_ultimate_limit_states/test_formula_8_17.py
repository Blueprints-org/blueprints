"""Testing formula 8.17 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_17 import (
    Form8Dot17ConfinedUltimateStrain,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot17ConfinedUltimateStrain:
    """Validation for formula 8.17 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_c2d = 5.0
        f_cd = 20.0

        # Object to test
        formula = Form8Dot17ConfinedUltimateStrain(sigma_c2d=sigma_c2d, f_cd=f_cd)

        # Expected result, manually calculated: 0.0035 + 0.2 * 5 / 20
        manually_calculated_result = 0.0535

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_sigma_c2d_is_negative(self) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot17ConfinedUltimateStrain(sigma_c2d=-5.0, f_cd=20.0)

    @pytest.mark.parametrize(
        "f_cd",
        [
            -20.0,  # f_cd is negative
            0.0,  # f_cd is zero
        ],
    )
    def test_raise_error_when_f_cd_is_less_or_equal_to_zero(self, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot17ConfinedUltimateStrain(sigma_c2d=5.0, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\varepsilon_{cu,c} = \varepsilon_{cu} + 0.2 \cdot \frac{\sigma_{c2d}}{f_{cd}} = "
                    r"0.0035 + 0.2 \cdot \frac{5.000}{20.000} = 0.054 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\varepsilon_{cu,c} = \varepsilon_{cu} + 0.2 \cdot \frac{\sigma_{c2d}}{f_{cd}} = "
                    r"0.0035 + 0.2 \cdot \frac{5.000 \ MPa}{20.000 \ MPa} = 0.054 \ -"
                ),
            ),
            ("short", r"\varepsilon_{cu,c} = 0.054 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_c2d = 5.0
        f_cd = 20.0

        # Object to test
        latex = Form8Dot17ConfinedUltimateStrain(sigma_c2d=sigma_c2d, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
