"""Testing the fatigue strength evaluator from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength import Form7FatigueStrength
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7FatigueStrength:
    """Validation for the fatigue strength evaluator from EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "expected"),
        [
            (FatigueStrengthCurve.FIG_7_1, 160.0, 1e6, 201.58737),  # first branch (slope m=3), N < N_D
            (FatigueStrengthCurve.FIG_7_1, 160.0, 2e6, 160.00000),  # detail category reference point N_C -> Δσ_C
            (FatigueStrengthCurve.FIG_7_1, 160.0, 5e6, 117.88901),  # N_D boundary -> Δσ_D = 0.737·Δσ_C
            (FatigueStrengthCurve.FIG_7_1, 160.0, 2e7, 89.34316),  # second branch (slope m=5), N_D < N < N_L
            (FatigueStrengthCurve.FIG_7_1, 160.0, 5e8, 64.75411),  # cut-off, N > N_L -> Δσ_L (constant)
            (FatigueStrengthCurve.FIG_7_2, 100.0, 1e6, 114.86984),  # shear, single slope (m=5)
            (FatigueStrengthCurve.FIG_7_2, 100.0, 1e8, 45.73051),  # shear, N_L boundary -> Δτ_L = 0.457·Δτ_C
            (FatigueStrengthCurve.FIG_7_2, 100.0, 2e8, 45.73051),  # shear, beyond N_L -> Δτ_L (constant)
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, expected: float) -> None:
        """Test the evaluation of the fatigue strength on each branch of the curve."""
        form = Form7FatigueStrength(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles)
        assert form == pytest.approx(expected=expected, rel=1e-5)

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            Form7FatigueStrength(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_7_1, n_cycles=1e6)

    @pytest.mark.parametrize("n_cycles", [0.0, -1e6])
    def test_raise_error_if_n_cycles_not_positive(self, n_cycles: DIMENSIONLESS) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive number of cycles."""
        with pytest.raises(LessOrEqualToZeroError):
            Form7FatigueStrength(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1, n_cycles=n_cycles)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                1e6,
                "complete",
                r"\Delta\sigma_{R} = \Delta\sigma_{C} \left( \frac{N_{C}}{N} \right)^{1 / m} = "
                r"160.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 3} = 201.587 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 1e6, "short", r"\Delta\sigma_{R} = 201.587 \ MPa"),
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                2e7,
                "complete",
                r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N} \right)^{1 / m} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{2.0 \cdot 10^{7}} \right)^{1 / 5} = 89.343 \ MPa",
            ),
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                5e8,
                "complete",
                r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa",
            ),
            (
                FatigueStrengthCurve.FIG_7_2,
                100.0,
                1e6,
                "complete",
                r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N} \right)^{1 / m} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 5} = 114.870 \ MPa",
            ),
            (
                FatigueStrengthCurve.FIG_7_2,
                100.0,
                2e8,
                "complete",
                r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{L}} \right)^{1 / m} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_7_2, 100.0, 2e8, "short", r"\Delta\tau_{R} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (direct) vs Δτ (shear) symbol switch."""
        latex = Form7FatigueStrength(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
