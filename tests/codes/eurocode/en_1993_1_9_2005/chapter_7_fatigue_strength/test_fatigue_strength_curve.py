"""Testing the standard fatigue strength curves from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import (
    FatigueStrengthCurve,
    StressType,
)
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve_value import Form7FatigueStrengthCurveValue


class TestFatigueStrengthCurve:
    """Validation for the standard fatigue strength curves of EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("curve", "stress_type", "description", "m1", "n_d", "m2", "n_l"),
        [
            (FatigueStrengthCurve.FIG_7_1, StressType.DIRECT, "Direct stress ranges (Figure 7.1)", 3.0, 5e6, 5.0, 1e8),
            (FatigueStrengthCurve.FIG_7_2, StressType.SHEAR, "Shear stress ranges (Figure 7.2)", 5.0, None, None, 1e8),
        ],
    )
    def test_member_constants(
        self,
        curve: FatigueStrengthCurve,
        stress_type: StressType,
        description: str,
        m1: float,
        n_d: float | None,
        m2: float | None,
        n_l: float,
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
            (FatigueStrengthCurve.FIG_7_1, True),
            (FatigueStrengthCurve.FIG_7_2, False),
        ],
    )
    def test_has_constant_amplitude_fatigue_limit(self, curve: FatigueStrengthCurve, expected: bool) -> None:
        """Test that only the shear curve (Figure 7.2) has no constant amplitude fatigue limit."""
        assert curve.has_constant_amplitude_fatigue_limit is expected

    def test_direct_stress_factors_match_standard(self) -> None:
        """Cross-check the stored geometry of Figure 7.1 against the published 0.737 and 0.549 factors of 7.1(2) and 7.1(3)."""
        curve = FatigueStrengthCurve.FIG_7_1
        assert curve.n_d is not None
        assert curve.m2 is not None

        delta_sigma_d = Form7FatigueStrengthCurveValue(
            delta_sigma_ref=1.0, n_ref=curve.n_c, n_target=curve.n_d, m=curve.m1, point="D", stress_type=curve.stress_type
        )
        assert float(delta_sigma_d) == pytest.approx(expected=0.737, rel=1e-3)

        delta_sigma_l = Form7FatigueStrengthCurveValue(
            delta_sigma_ref=float(delta_sigma_d), n_ref=curve.n_d, n_target=curve.n_l, m=curve.m2, point="L", stress_type=curve.stress_type
        )
        assert float(delta_sigma_l) / float(delta_sigma_d) == pytest.approx(expected=0.549, rel=1e-3)

    def test_shear_factor_matches_standard(self) -> None:
        """Cross-check the stored geometry of Figure 7.2 against the published 0.457 factor of 7.1(2)."""
        curve = FatigueStrengthCurve.FIG_7_2

        delta_tau_l = Form7FatigueStrengthCurveValue(
            delta_sigma_ref=1.0, n_ref=curve.n_c, n_target=curve.n_l, m=curve.m1, point="L", stress_type=curve.stress_type
        )
        assert float(delta_tau_l) == pytest.approx(expected=0.457, rel=1e-3)
