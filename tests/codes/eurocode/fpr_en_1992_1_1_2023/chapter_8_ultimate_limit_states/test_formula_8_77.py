"""Testing formula 8.77 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_77 import (
    Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError

# The example is a rough interface according to Table 8.2, with C30/37 concrete and B500B reinforcement.
DEFAULTS = {
    "c_v2": 0.08,
    "f_ck": 30.0,
    "gamma_c": 1.5,
    "mu_v": 0.7,
    "sigma_n": 2.0,
    "k_v": 0.5,
    "rho_i": 0.005,
    "f_yd": 435.0,
    "k_dowel": 0.9,
    "f_cd": 20.0,
}


class TestForm8Dot77ShearStressResistanceAtInterfaceWithoutYielding:
    """Validation for formula 8.77 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result where the printed expression governs."""
        # Object to test
        formula = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**DEFAULTS)

        # Expected result, manually calculated: the four terms are 0.292119, 1.4, 0.76125 and 0.419732,
        # against an upper bound of 0.25 * 20 = 5.0
        manually_calculated_result = 2.873101  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_where_the_upper_bound_governs(self) -> None:
        """Tests the upper bound that the standard prints on the same line."""
        # Object to test
        formula = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, "rho_i": 0.05})

        # Expected result, manually calculated: the expression reaches 13.501939 while the upper bound stays
        # at a quarter of f_cd
        manually_calculated_result = 5.0  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_a_tensile_normal_stress(self) -> None:
        """Tests the rule of art. 8.2.6(5) that takes the term with a tensile normal stress as zero."""
        # Object to test
        formula = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, "sigma_n": -2.0})

        # Expected result, manually calculated: the second term drops out and the remaining three give
        # 0.292119, 0.76125 and 0.419732
        manually_calculated_result = 1.473101  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_perpendicular_tension_and_the_table_footnote(self) -> None:
        """Tests the coherent design case for perpendicular tension.

        A negative normal stress is the condition of footnote a of Table 8.2, which sets the cohesion factor of a
        rough interface to zero, so both the first and the second term drop out and only the reinforcement terms
        remain. The class does not apply that footnote itself, so the zero is passed in, which is what a caller
        reading Table 8.2 would supply.
        """
        # Object to test
        formula = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, "c_v2": 0.0, "sigma_n": -2.0})

        # Expected result, manually calculated: only 0.76125 and 0.419732 are left
        manually_calculated_result = 1.180982  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_the_cap_on_the_normal_stress_is_applied(self) -> None:
        """Tests that a compressive normal stress is not taken larger than 0.60 f_cd.

        The factor is set to 0.05, below every value of Table 8.2, because only there does the cap change the
        result instead of being masked by the upper bound of the printed line.
        """
        # Objects to test, identical apart from a normal stress on and above the cap of 0.60 * 20 = 12
        at_the_cap = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, "mu_v": 0.05, "sigma_n": 12.0})
        above_the_cap = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, "mu_v": 0.05, "sigma_n": 15.0})

        # Expected result, manually calculated: the four terms are 0.292119, 0.6, 0.054375 and 0.419732
        manually_calculated_result = 1.366226  # MPa

        assert at_the_cap == pytest.approx(expected=manually_calculated_result, rel=1e-4)
        assert above_the_cap == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("c_v2", -0.08),  # c_v2 is negative
            ("f_ck", -30.0),  # f_ck is negative
            ("mu_v", -0.7),  # mu_v is negative
            ("k_v", -0.5),  # k_v is negative
            ("rho_i", -0.005),  # rho_i is negative
            ("f_yd", -435.0),  # f_yd is negative
            ("k_dowel", -0.9),  # k_dowel is negative
            ("f_cd", -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, field: str, value: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, field: value})

    @pytest.mark.parametrize("gamma_c", [-1.5, 0.0])
    def test_raise_error_when_gamma_c_is_not_positive(self, gamma_c: float) -> None:
        """Test invalid values of the partial factor."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**{**DEFAULTS, "gamma_c": gamma_c})

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rdi} = \min\left(c_{v2} \cdot \frac{\sqrt{f_{ck}}}{\gamma_C} + \mu_v \cdot "
                    r"\min\left(\max\left(\sigma_n, 0\right), 0.60 \cdot f_{cd}\right) + "
                    r"k_v \cdot \rho_i \cdot f_{yd} \cdot \mu_v + "
                    r"k_{dowel} \cdot \rho_i \cdot \sqrt{f_{yd} \cdot f_{cd}}, 0.25 \cdot f_{cd}\right) = "
                    r"\min\left(0.080 \cdot \frac{\sqrt{30.000}}{1.500} + 0.700 \cdot "
                    r"\min\left(\max\left(2.000, 0\right), 0.60 \cdot 20.000\right) + "
                    r"0.500 \cdot 0.005 \cdot 435.000 \cdot 0.700 + "
                    r"0.900 \cdot 0.005 \cdot \sqrt{435.000 \cdot 20.000}, 0.25 \cdot 20.000\right) = 2.873 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rdi} = \min\left(c_{v2} \cdot \frac{\sqrt{f_{ck}}}{\gamma_C} + \mu_v \cdot "
                    r"\min\left(\max\left(\sigma_n, 0\right), 0.60 \cdot f_{cd}\right) + "
                    r"k_v \cdot \rho_i \cdot f_{yd} \cdot \mu_v + "
                    r"k_{dowel} \cdot \rho_i \cdot \sqrt{f_{yd} \cdot f_{cd}}, 0.25 \cdot f_{cd}\right) = "
                    r"\min\left(0.080 \cdot \frac{\sqrt{30.000 \ MPa}}{1.500} + 0.700 \cdot "
                    r"\min\left(\max\left(2.000 \ MPa, 0\right), 0.60 \cdot 20.000 \ MPa\right) + "
                    r"0.500 \cdot 0.005 \cdot 435.000 \ MPa \cdot 0.700 + "
                    r"0.900 \cdot 0.005 \cdot \sqrt{435.000 \ MPa \cdot 20.000 \ MPa}, 0.25 \cdot 20.000 \ MPa\right) = 2.873 \ MPa"
                ),
            ),
            ("short", r"\tau_{Rdi} = 2.873 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot77ShearStressResistanceAtInterfaceWithoutYielding(**DEFAULTS).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
