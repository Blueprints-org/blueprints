"""Testing formula 8.76 of FprEN 1992-1-1:2023."""

import pytest

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.formula_8_76 import (
    Form8Dot76ShearStressResistanceAtInterface,
)
from blueprints.codes.eurocode.fpr_en_1992_1_1_2023.chapter_8_ultimate_limit_states.table_8_2 import (
    SurfaceRoughness,
    Table8Dot2CoefficientsSurfaceRoughness,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError

# The example is a rough interface according to Table 8.2, with C30/37 concrete and B500B reinforcement.
DEFAULTS = {
    "c_v1": 0.15,
    "f_ck": 30.0,
    "gamma_c": 1.5,
    "mu_v": 0.7,
    "sigma_n": 2.0,
    "rho_i": 0.005,
    "f_yd": 435.0,
    "alpha": 60.0,
    "f_cd": 20.0,
}


class TestForm8Dot76ShearStressResistanceAtInterface:
    """Validation for formula 8.76 from FprEN 1992-1-1:2023."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result where the printed expression governs."""
        # Object to test
        formula = Form8Dot76ShearStressResistanceAtInterface(**DEFAULTS)

        # Expected result, manually calculated:
        # 0.15 * sqrt(30) / 1.5 + 0.7 * 2.0 + 0.005 * 435 * (0.7 * sin(60) + cos(60)) = 4.353746,
        # against an upper bound of 0.30 * 20 + 0.005 * 435 * cos(60) = 7.0875
        manually_calculated_result = 4.353746  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_where_the_upper_bound_governs(self) -> None:
        """Tests the upper bound that the standard prints on the same line."""
        # Object to test
        formula = Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "rho_i": 0.02})

        # Expected result, manually calculated: the expression reaches 11.571817 while the upper bound,
        # being thirty percent of f_cd plus the contribution of the reinforcement, stays at 10.35
        manually_calculated_result = 10.35  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_a_tensile_normal_stress(self) -> None:
        """Tests the rule that takes the term with a tensile normal stress as zero.

        The roughness factor is left at its printed value here to isolate that one rule. In a real design
        case perpendicular tension also triggers footnote a of Table 8.2, which is the next test.
        """
        # Object to test
        formula = Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "sigma_n": -2.0})

        # Expected result, manually calculated: the middle term drops out and the first and third terms
        # give 0.547723 and 2.406024
        manually_calculated_result = 2.953746  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_perpendicular_tension_and_the_table_footnote(self) -> None:
        """Tests the coherent design case for perpendicular tension, with the coefficient taken from Table 8.2.

        Footnote a of the table sets the roughness factor to zero for a rough interface under perpendicular
        tension, and the prose of Formula (8.76) drops the term with the normal stress, so only the
        reinforcement term remains.
        """
        table = Table8Dot2CoefficientsSurfaceRoughness(surface_roughness=SurfaceRoughness.ROUGH, tension_perpendicular_to_interface=True)

        # Object to test
        formula = Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "c_v1": table.c_v1, "mu_v": table.mu_v, "sigma_n": -2.0})

        # Expected result, manually calculated: only 0.005 * 435 * (0.7 * sin(60) + cos(60)) is left
        manually_calculated_result = 2.406024  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_with_a_normal_stress_above_its_cap(self) -> None:
        """Tests a compressive normal stress beyond the cap, where the upper bound of the printed line governs.

        With any factor from Table 8.2 the capped middle term already exhausts the first part of the upper
        bound, so the bound governs and the cap itself cannot change the answer. The next test shows the cap
        being applied, with a factor chosen outside the table to make it observable.
        """
        # Object to test
        formula = Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "sigma_n": 15.0})

        # Expected result, manually calculated: the expression reaches 11.353746 with the normal stress
        # capped at twelve, against an upper bound of 7.0875
        manually_calculated_result = 7.0875  # MPa

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_the_cap_on_the_normal_stress_is_applied(self) -> None:
        """Tests that a compressive normal stress is not taken larger than 0.60 f_cd.

        The factor is set to 0.1, below every value of Table 8.2, because only there does the cap change the
        result instead of being masked by the upper bound of the printed line.
        """
        # Objects to test, identical apart from a normal stress on and above the cap of 0.60 * 20 = 12
        at_the_cap = Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "mu_v": 0.1, "sigma_n": 12.0})
        above_the_cap = Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "mu_v": 0.1, "sigma_n": 15.0})

        # Expected result, manually calculated: 0.15 * sqrt(30) / 1.5 + 0.1 * 12 + 0.005 * 435 * (0.1 *
        # sin(60) + cos(60)), against an upper bound of 7.0875
        manually_calculated_result = 3.023583  # MPa

        assert at_the_cap == pytest.approx(expected=manually_calculated_result, rel=1e-4)
        assert above_the_cap == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("c_v1", -0.15),  # c_v1 is negative
            ("f_ck", -30.0),  # f_ck is negative
            ("mu_v", -0.7),  # mu_v is negative
            ("rho_i", -0.005),  # rho_i is negative
            ("f_yd", -435.0),  # f_yd is negative
            ("f_cd", -20.0),  # f_cd is negative
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, field: str, value: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, field: value})

    @pytest.mark.parametrize("gamma_c", [-1.5, 0.0])
    def test_raise_error_when_gamma_c_is_not_positive(self, gamma_c: float) -> None:
        """Test invalid values of the partial factor."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "gamma_c": gamma_c})

    @pytest.mark.parametrize("alpha", [34.9, 135.1])
    def test_raise_error_when_alpha_is_outside_the_printed_limits(self, alpha: float) -> None:
        """Test angles outside the range that the standard allows."""
        with pytest.raises(ValueError, match="Invalid angle alpha"):
            Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "alpha": alpha})

    @pytest.mark.parametrize("alpha", [35.0, 135.0])
    def test_alpha_on_the_printed_limits_is_accepted(self, alpha: float) -> None:
        """Both bounds on the angle are inclusive as printed."""
        assert Form8Dot76ShearStressResistanceAtInterface(**{**DEFAULTS, "alpha": alpha}) > 0

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\tau_{Rdi} = \min\left(c_{v1} \cdot \frac{\sqrt{f_{ck}}}{\gamma_C} + \mu_v \cdot "
                    r"\min\left(\max\left(\sigma_n, 0\right), 0.60 \cdot f_{cd}\right) + "
                    r"\rho_i \cdot f_{yd} \cdot \left(\mu_v \cdot \sin\alpha + \cos\alpha\right), "
                    r"0.30 \cdot f_{cd} + \rho_i \cdot f_{yd} \cdot \cos\alpha\right) = "
                    r"\min\left(0.150 \cdot \frac{\sqrt{30.000}}{1.500} + 0.700 \cdot "
                    r"\min\left(\max\left(2.000, 0\right), 0.60 \cdot 20.000\right) + "
                    r"0.005 \cdot 435.000 \cdot \left(0.700 \cdot \sin60.000 + \cos60.000\right), "
                    r"0.30 \cdot 20.000 + 0.005 \cdot 435.000 \cdot \cos60.000\right) = 4.354 \ MPa"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\tau_{Rdi} = \min\left(c_{v1} \cdot \frac{\sqrt{f_{ck}}}{\gamma_C} + \mu_v \cdot "
                    r"\min\left(\max\left(\sigma_n, 0\right), 0.60 \cdot f_{cd}\right) + "
                    r"\rho_i \cdot f_{yd} \cdot \left(\mu_v \cdot \sin\alpha + \cos\alpha\right), "
                    r"0.30 \cdot f_{cd} + \rho_i \cdot f_{yd} \cdot \cos\alpha\right) = "
                    r"\min\left(0.150 \cdot \frac{\sqrt{30.000 \ MPa}}{1.500} + 0.700 \cdot "
                    r"\min\left(\max\left(2.000 \ MPa, 0\right), 0.60 \cdot 20.000 \ MPa\right) + "
                    r"0.005 \cdot 435.000 \ MPa \cdot \left(0.700 \cdot \sin60.000 \ deg + \cos60.000 \ deg\right), "
                    r"0.30 \cdot 20.000 \ MPa + 0.005 \cdot 435.000 \ MPa \cdot \cos60.000 \ deg\right) = 4.354 \ MPa"
                ),
            ),
            ("short", r"\tau_{Rdi} = 4.354 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Object to test
        latex = Form8Dot76ShearStressResistanceAtInterface(**DEFAULTS).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
