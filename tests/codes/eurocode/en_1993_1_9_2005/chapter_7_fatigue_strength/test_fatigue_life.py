"""Testing the fatigue life evaluator from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

import math

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_life import Form7FatigueLife
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength import Form7FatigueStrength
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.validations import NegativeValueError


class TestForm7FatigueLife:
    """Validation for the fatigue life evaluator from EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles"),
        [
            (FatigueStrengthCurve.FIG_7_1, 160.0, 1e6),  # first branch (slope m=3), N < N_D
            (FatigueStrengthCurve.FIG_7_1, 160.0, 5e6),  # N_D boundary -> Δσ_D maps back to N_D
            (FatigueStrengthCurve.FIG_7_1, 160.0, 2e7),  # second branch (slope m=5), N_D < N < N_L
            (FatigueStrengthCurve.FIG_7_1, 160.0, 1e8),  # N_L boundary -> Δσ_L maps back to N_L
            (FatigueStrengthCurve.FIG_7_2, 100.0, 1e6),  # shear, single slope
            (FatigueStrengthCurve.FIG_7_2, 100.0, 1e8),  # shear, N_L boundary -> Δτ_L maps back to N_L
        ],
    )
    def test_inverts_fatigue_strength(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float) -> None:
        """The fatigue life is the inverse of the fatigue strength: reading Δσ_R at N and feeding it back returns N."""
        delta_sigma_r = float(Form7FatigueStrength(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles))

        life = Form7FatigueLife(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert life == pytest.approx(expected=n_cycles, rel=1e-6)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r", "expected"),
        [
            (FatigueStrengthCurve.FIG_7_1, 160.0, 160.0, 2e6),  # Δσ_R = Δσ_C maps to the reference point N_C
            (FatigueStrengthCurve.FIG_7_1, 160.0, 320.0, 2e6 / 8),  # halving the life-cube: N_R = N_C (Δσ_C/Δσ_R)^3
            (FatigueStrengthCurve.FIG_7_2, 100.0, 100.0, 2e6),  # shear, Δτ_R = Δτ_C maps to N_C
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float, expected: float) -> None:
        """Test the evaluation against directly computed reference points."""
        life = Form7FatigueLife(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert life == pytest.approx(expected=expected, rel=1e-9)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r"),
        [
            (FatigueStrengthCurve.FIG_7_1, 160.0, 60.0),  # below the cut-off limit Δσ_L = 64.75
            (FatigueStrengthCurve.FIG_7_1, 160.0, 0.0),  # a zero stress range never accumulates damage
            (FatigueStrengthCurve.FIG_7_2, 100.0, 40.0),  # shear, below the cut-off limit Δτ_L = 45.73
        ],
    )
    def test_infinite_life_below_cutoff(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float) -> None:
        """Below the cut-off limit the life is infinite, i.e. no fatigue damage."""
        life = Form7FatigueLife(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert math.isinf(life)

    @pytest.mark.parametrize(
        ("delta_sigma_r", "expected_point", "expected_m"),
        [
            (201.587, "C", 3.0),  # first branch
            (89.343, "D", 5.0),  # second branch
            (60.0, "L", None),  # below the cut-off limit
        ],
    )
    def test_detailed_result_reports_governing_branch(self, delta_sigma_r: float, expected_point: str, expected_m: float | None) -> None:
        """The detailed result exposes which branch governs, so callers can label N_R without re-deriving it."""
        detail = Form7FatigueLife(delta_sigma_r=delta_sigma_r, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1).detailed_result

        assert detail["reference_point"] == expected_point
        assert detail["m"] == expected_m

    def test_detailed_result_shear_curve_anchors_at_cutoff_limit(self) -> None:
        """For the single-slope shear curve, the cut-off anchor is the cut-off limit (Δτ_L, N_L).

        Unlike the direct stress curve, the shear curve (Figure 7.2) has no constant amplitude fatigue limit: its
        single slope runs straight to the cut-off limit Δτ_L at N_L. So below Δτ_L the life is infinite and the
        detailed result reports the cut-off point itself as the governing reference (point "L", slope None).
        """
        curve = FatigueStrengthCurve.FIG_7_2
        detail = Form7FatigueLife(delta_sigma_r=40.0, delta_sigma_c=100.0, curve=curve).detailed_result

        assert detail["reference_point"] == "L"
        assert detail["m"] is None
        assert detail["delta_sigma_ref"] == pytest.approx(45.730505, rel=1e-6)  # Δτ_L = 0.457·Δτ_C
        assert detail["n_ref"] == pytest.approx(curve.n_l)  # the cut-off cycle number N_L = 1e8
        assert math.isinf(detail["n_r"])

    def test_raise_error_if_negative_delta_sigma_r(self) -> None:
        """Test that a NegativeValueError is raised when the applied stress range is negative."""
        with pytest.raises(NegativeValueError):
            Form7FatigueLife(delta_sigma_r=-160.0, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when the detail category is negative."""
        with pytest.raises(NegativeValueError):
            Form7FatigueLife(delta_sigma_r=160.0, delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                201.587,
                "complete",
                r"N_{R} = N_{C} \left( \frac{\Delta\sigma_{C}}{\Delta\sigma_{R}} \right)^{m} = "
                r"2.0 \cdot 10^{6} \left( \frac{160.000}{201.587} \right)^{3} = 1000005",
            ),
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                89.343,
                "complete",
                r"N_{R} = N_{D} \left( \frac{\Delta\sigma_{D}}{\Delta\sigma_{R}} \right)^{m} = "
                r"5.0 \cdot 10^{6} \left( \frac{117.889}{89.343} \right)^{5} = 20000180",
            ),
            (
                FatigueStrengthCurve.FIG_7_2,
                100.0,
                114.870,
                "complete",
                r"N_{R} = N_{C} \left( \frac{\Delta\tau_{C}}{\Delta\tau_{R}} \right)^{m} = "
                r"2.0 \cdot 10^{6} \left( \frac{100.000}{114.870} \right)^{5} = 999993",
            ),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 201.587, "short", r"N_{R} = 1000005"),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 60.0, "complete", r"N_{R} = \infty"),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 60.0, "short", r"N_{R} = \infty"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (direct) vs Δτ (shear) symbol switch and infinite life."""
        latex = Form7FatigueLife(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
