"""Testing formulas 8.9 and 8.10 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_9_10 import (
    Form8Dot9To10ConcreteStrengthIncreaseConfinement,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8Dot9To10ConcreteStrengthIncreaseConfinement:
    """Validation for formulas 8.9 and 8.10 from FprEN 1992-1-1:2023."""

    def test_evaluation_low_stress_branch(self) -> None:
        """Tests the evaluation of the result on the low-stress branch, formula (8.9), without reduction."""
        # Example values
        sigma_c2d = 5.0
        f_cd = 20.0
        d_dg = 32.0

        # Object to test
        formula = Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=sigma_c2d, f_cd=f_cd, d_dg=d_dg)

        # Expected result, manually calculated: 4 * 5 * min(32 / 32, 1.0)
        manually_calculated_result = 20.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_high_stress_branch(self) -> None:
        """Tests the evaluation of the result on the high-stress branch, formula (8.10), without reduction."""
        # Example values
        sigma_c2d = 15.0
        f_cd = 20.0
        d_dg = 32.0

        # Object to test
        formula = Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=sigma_c2d, f_cd=f_cd, d_dg=d_dg)

        # Expected result, manually calculated: 3.5 * 15**(3/4) * 20**(1/4) * min(32 / 32, 1.0)
        manually_calculated_result = 56.41492142073595

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_at_boundary(self) -> None:
        """Tests the evaluation of the result exactly at the boundary, where the low-stress branch governs."""
        # Example values
        sigma_c2d = 12.0
        f_cd = 20.0
        d_dg = 32.0

        # Object to test
        formula = Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=sigma_c2d, f_cd=f_cd, d_dg=d_dg)

        # Expected result, manually calculated: 4 * 12 (the low-stress branch, since sigma_c2d = 0.6 * f_cd)
        manually_calculated_result = 48.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_reduction_factor(self) -> None:
        """Tests the evaluation of the result where d_dg < 32 mm and the reduction factor applies."""
        # Example values
        sigma_c2d = 5.0
        f_cd = 20.0
        d_dg = 16.0

        # Object to test
        formula = Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=sigma_c2d, f_cd=f_cd, d_dg=d_dg)

        # Expected result, manually calculated: 4 * 5 * (16 / 32)
        manually_calculated_result = 10.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sigma_c2d", "f_cd"),
        [
            (-5.0, 20.0),  # sigma_c2d is negative
            (5.0, -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, sigma_c2d: float, f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=sigma_c2d, f_cd=f_cd, d_dg=32.0)

    @pytest.mark.parametrize(
        "d_dg",
        [
            -32.0,  # d_dg is negative
            0.0,  # d_dg is zero
        ],
    )
    def test_raise_error_when_d_dg_is_less_or_equal_to_zero(self, d_dg: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=5.0, f_cd=20.0, d_dg=d_dg)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\Delta f_{cd} = \min\left(\frac{d_{dg}}{32}, 1.0\right) \cdot "
                    r"\begin{cases} 4 \cdot \sigma_{c2d} & \text{for } \sigma_{c2d} \leq 0.6 \cdot f_{cd} \\ "
                    r"3.5 \cdot \left(\sigma_{c2d}\right)^{3/4} \cdot \left(f_{cd}\right)^{1/4} & "
                    r"\text{for } \sigma_{c2d} > 0.6 \cdot f_{cd} \end{cases} = "
                    r"\min\left(\frac{32.000}{32}, 1.0\right) \cdot "
                    r"\begin{cases} 4 \cdot 5.000 & \text{for } 5.000 \leq 0.6 \cdot 20.000 \\ "
                    r"3.5 \cdot \left(5.000\right)^{3/4} \cdot \left(20.000\right)^{1/4} & "
                    r"\text{for } 5.000 > 0.6 \cdot 20.000 \end{cases} = 20.000 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\Delta f_{cd} = \min\left(\frac{d_{dg}}{32}, 1.0\right) \cdot "
                    r"\begin{cases} 4 \cdot \sigma_{c2d} & \text{for } \sigma_{c2d} \leq 0.6 \cdot f_{cd} \\ "
                    r"3.5 \cdot \left(\sigma_{c2d}\right)^{3/4} \cdot \left(f_{cd}\right)^{1/4} & "
                    r"\text{for } \sigma_{c2d} > 0.6 \cdot f_{cd} \end{cases} = "
                    r"\min\left(\frac{32.000 \ mm}{32}, 1.0\right) \cdot "
                    r"\begin{cases} 4 \cdot 5.000 \ MPa & \text{for } 5.000 \ MPa \leq 0.6 \cdot 20.000 \ MPa \\ "
                    r"3.5 \cdot \left(5.000 \ MPa\right)^{3/4} \cdot \left(20.000 \ MPa\right)^{1/4} & "
                    r"\text{for } 5.000 \ MPa > 0.6 \cdot 20.000 \ MPa \end{cases} = 20.000 \ MPa"
                ),
            ),
            ("short", r"\Delta f_{cd} = 20.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_c2d = 5.0
        f_cd = 20.0
        d_dg = 32.0

        # Object to test
        latex = Form8Dot9To10ConcreteStrengthIncreaseConfinement(sigma_c2d=sigma_c2d, f_cd=f_cd, d_dg=d_dg).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
