"""Testing the fatigue strength evaluator from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength import Form8FatigueStrength
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm8FatigueStrength:
    """Validation for the fatigue strength evaluator from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "expected"),
        [
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e6, 201.58737),  # first branch (slope m1), N < N_D
            (FatigueStrengthCurve.FIG_8_1B, 160.0, 2e6, 160.00000),  # N_C = N_D boundary -> Δσ_D = Δσ_C
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 2e7, 89.34316),  # second branch (slope m2), N_D < N < N_L
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 5e8, 64.75411),  # cut-off, N > N_L -> Δσ_L (constant)
            (FatigueStrengthCurve.FIG_8_4, 100.0, 1e6, 114.86984),  # shear, first branch
            (FatigueStrengthCurve.FIG_8_4, 100.0, 2e8, 45.73051),  # shear, beyond N_D -> Δτ_D (constant)
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, expected: float) -> None:
        """Test the evaluation of the fatigue strength on each branch of the curve."""
        form = Form8FatigueStrength(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles)
        assert form == pytest.approx(expected=expected, rel=1e-5)

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            Form8FatigueStrength(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=1e6)

    @pytest.mark.parametrize("n_cycles", [0.0, -1e6])
    def test_raise_error_if_n_cycles_not_positive(self, n_cycles: DIMENSIONLESS) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive number of cycles."""
        with pytest.raises(LessOrEqualToZeroError):
            Form8FatigueStrength(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=n_cycles)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                1e6,
                "complete",
                r"\Delta\sigma_{R} = \Delta\sigma_{C} \left( \frac{N_{C}}{N} \right)^{1 / m_{1}} = "
                r"160.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 3} = 201.587 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e6, "short", r"\Delta\sigma_{R} = 201.587 \ MPa"),
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                2e7,
                "complete",
                r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N} \right)^{1 / m_{2}} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{2.0 \cdot 10^{7}} \right)^{1 / 5} = 89.343 \ MPa",
            ),
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                5e8,
                "complete",
                r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m_{2}} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa",
            ),
            (
                FatigueStrengthCurve.FIG_8_4,
                100.0,
                1e6,
                "complete",
                r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N} \right)^{1 / m_{1}} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 5} = 114.870 \ MPa",
            ),
            (
                FatigueStrengthCurve.FIG_8_4,
                100.0,
                2e8,
                "complete",
                r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_8_4, 100.0, 2e8, "short", r"\Delta\tau_{R} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (normal) vs Δτ (shear) symbol switch."""
        latex = Form8FatigueStrength(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
