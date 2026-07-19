"""Testing the standard fatigue strength curves from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import (
    FatigueStrengthCurve,
    StressType,
)
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_value import Form8FatigueStrengthCurveValue


class TestFatigueStrengthCurve:
    """Validation for the standard fatigue strength curves of EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "stress_type", "description", "m1", "n_d", "m2", "n_l"),
        [
            (FatigueStrengthCurve.FIG_8_1A, StressType.NORMAL, "Non-welded details, light notch effect (Figure 8.1a)", 5.0, 2e6, 9.0, 1e8),
            (FatigueStrengthCurve.FIG_8_1B, StressType.NORMAL, "Non-welded details, sharp notch effect (Figure 8.1b)", 3.0, 2e6, 5.0, 1e8),
            (FatigueStrengthCurve.FIG_8_2A, StressType.NORMAL, "Welded details, detail category 71 and above (Figure 8.2a)", 3.0, 5e6, 5.0, 1e8),
            (FatigueStrengthCurve.FIG_8_2B, StressType.NORMAL, "Welded details, detail category below 71 (Figure 8.2b)", 3.0, 1e7, 5.0, 1e8),
            (
                FatigueStrengthCurve.FIG_8_3,
                StressType.NORMAL,
                "Lattice girder joints of hollow sections, Table 10.8 (Figure 8.3)",
                5.0,
                1e7,
                9.0,
                1e8,
            ),
            (FatigueStrengthCurve.FIG_8_4, StressType.SHEAR, "Constructional details subject to shear stress (Figure 8.4)", 5.0, 1e8, None, None),
        ],
    )
    def test_member_constants(
        self,
        curve: FatigueStrengthCurve,
        stress_type: StressType,
        description: str,
        m1: float,
        n_d: float,
        m2: float | None,
        n_l: float | None,
    ) -> None:
        """Test that every curve member carries the geometry of its figure, and the shared reference point N_C."""
        assert curve.stress_type is stress_type
        assert curve.description == description
        assert curve.m1 == m1
        assert curve.n_c == 2e6
        assert curve.n_d == n_d
        assert curve.m2 == m2
        assert curve.n_l == n_l

    @pytest.mark.parametrize(
        ("curve", "expected"),
        [
            (FatigueStrengthCurve.FIG_8_1A, True),
            (FatigueStrengthCurve.FIG_8_1B, True),
            (FatigueStrengthCurve.FIG_8_2A, True),
            (FatigueStrengthCurve.FIG_8_2B, True),
            (FatigueStrengthCurve.FIG_8_3, True),
            (FatigueStrengthCurve.FIG_8_4, False),
        ],
    )
    def test_has_cutoff_segment(self, curve: FatigueStrengthCurve, expected: bool) -> None:
        """Test that only the shear curve (Figure 8.4) has no separate cut-off branch."""
        assert curve.has_cutoff_segment is expected

    @pytest.mark.parametrize(
        ("curve", "d_over_c", "l_over_c"),
        [
            (FatigueStrengthCurve.FIG_8_1A, 1.000, 0.647),
            (FatigueStrengthCurve.FIG_8_1B, 1.000, 0.457),
            (FatigueStrengthCurve.FIG_8_2A, 0.737, 0.405),
            (FatigueStrengthCurve.FIG_8_2B, 0.585, 0.369),
            (FatigueStrengthCurve.FIG_8_3, 0.725, 0.561),
            (FatigueStrengthCurve.FIG_8_4, 0.457, None),
        ],
    )
    def test_factors_match_standard(self, curve: FatigueStrengthCurve, d_over_c: float, l_over_c: float | None) -> None:
        """Cross-check the stored geometry against the published Δσ_D/Δσ_C and Δσ_L/Δσ_C factors of Figures 8.1 - 8.4."""
        delta_sigma_d = Form8FatigueStrengthCurveValue(delta_sigma_ref=1.0, n_ref=curve.n_c, n_target=curve.n_d, m=curve.m1, point="D")
        assert float(delta_sigma_d) == pytest.approx(expected=d_over_c, rel=1e-3)

        if curve.m2 is not None and curve.n_l is not None:
            delta_sigma_l = Form8FatigueStrengthCurveValue(delta_sigma_ref=delta_sigma_d, n_ref=curve.n_d, n_target=curve.n_l, m=curve.m2, point="L")
            assert float(delta_sigma_l) == pytest.approx(expected=l_over_c, rel=1e-3)
        else:
            assert l_over_c is None
