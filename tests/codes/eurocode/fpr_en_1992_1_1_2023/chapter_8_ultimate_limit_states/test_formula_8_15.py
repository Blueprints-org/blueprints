"""Testing formula 8.15 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_15 import (
    Form8Dot15AverageConfinedConcreteStrength,
)
from blueprints.validations import NegativeValueError


class TestForm8Dot15AverageConfinedConcreteStrength:
    """Validation for formula 8.15 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        f_cd = 20.0
        k_conf_b = 0.5
        k_conf_s = 0.8
        delta_f_cd = 10.0

        # Object to test
        formula = Form8Dot15AverageConfinedConcreteStrength(f_cd=f_cd, k_conf_b=k_conf_b, k_conf_s=k_conf_s, delta_f_cd=delta_f_cd)

        # Expected result, manually calculated: 20 + 0.5 * 0.8 * 10
        manually_calculated_result = 24.0

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("f_cd", "k_conf_b", "k_conf_s", "delta_f_cd"),
        [
            (-20.0, 0.5, 0.8, 10.0),  # f_cd is negative
            (20.0, -0.5, 0.8, 10.0),  # k_conf_b is negative
            (20.0, 0.5, -0.8, 10.0),  # k_conf_s is negative
            (20.0, 0.5, 0.8, -10.0),  # delta_f_cd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, f_cd: float, k_conf_b: float, k_conf_s: float, delta_f_cd: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot15AverageConfinedConcreteStrength(f_cd=f_cd, k_conf_b=k_conf_b, k_conf_s=k_conf_s, delta_f_cd=delta_f_cd)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"f_{cd,c} = f_{cd} + k_{conf,b} \cdot k_{conf,s} \cdot \Delta f_{cd} = 20.000 + 0.500 \cdot 0.800 \cdot 10.000 = 24.000 \ MPa",
            ),
            (
                "complete_with_units",
                (
                    r"f_{cd,c} = f_{cd} + k_{conf,b} \cdot k_{conf,s} \cdot \Delta f_{cd} = "
                    r"20.000 \ MPa + 0.500 \cdot 0.800 \cdot 10.000 \ MPa = 24.000 \ MPa"
                ),
            ),
            ("short", r"f_{cd,c} = 24.000 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        f_cd = 20.0
        k_conf_b = 0.5
        k_conf_s = 0.8
        delta_f_cd = 10.0

        # Object to test
        latex = Form8Dot15AverageConfinedConcreteStrength(f_cd=f_cd, k_conf_b=k_conf_b, k_conf_s=k_conf_s, delta_f_cd=delta_f_cd).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
