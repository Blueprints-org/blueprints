"""Testing formula 8.16 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_16 import (
    Form8Dot16ConfinedStrainAtPeakStress,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot16ConfinedStrainAtPeakStress:
    """Validation for formula 8.16 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        delta_f_cd = 10.0
        f_cd = 20.0

        # Object to test
        formula = Form8Dot16ConfinedStrainAtPeakStress(delta_f_cd=delta_f_cd, f_cd=f_cd)

        # Expected result, manually calculated: 0.002 * (1 + 5 * 10 / 20)
        manually_calculated_result = 0.007

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_raise_error_when_delta_f_cd_is_negative(self) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot16ConfinedStrainAtPeakStress(delta_f_cd=-10.0, f_cd=20.0)

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
            Form8Dot16ConfinedStrainAtPeakStress(delta_f_cd=10.0, f_cd=f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\varepsilon_{c2,c} = \varepsilon_{c2} \cdot \left(1 + 5 \cdot \frac{\Delta f_{cd}}{f_{cd}}\right) = "
                    r"0.002 \cdot \left(1 + 5 \cdot \frac{10.000}{20.000}\right) = 0.007 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\varepsilon_{c2,c} = \varepsilon_{c2} \cdot \left(1 + 5 \cdot \frac{\Delta f_{cd}}{f_{cd}}\right) = "
                    r"0.002 \cdot \left(1 + 5 \cdot \frac{10.000 \ MPa}{20.000 \ MPa}\right) = 0.007 \ -"
                ),
            ),
            ("short", r"\varepsilon_{c2,c} = 0.007 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        delta_f_cd = 10.0
        f_cd = 20.0

        # Object to test
        latex = Form8Dot16ConfinedStrainAtPeakStress(delta_f_cd=delta_f_cd, f_cd=f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
