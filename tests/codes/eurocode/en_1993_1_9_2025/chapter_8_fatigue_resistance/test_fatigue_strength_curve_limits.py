"""Testing the fatigue strength curve limits from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength import Form8FatigueStrength
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_limits import FatigueStrengthCurveLimits
from blueprints.validations import NegativeValueError


class TestFatigueStrengthCurveLimits:
    """Validation for the fatigue strength curve limits from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "d_over_c", "l_over_c"),
        [
            (FatigueStrengthCurve.FIG_8_1A, 160.0, 1.000, 0.647),
            (FatigueStrengthCurve.FIG_8_1B, 160.0, 1.000, 0.457),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 0.737, 0.405),
            (FatigueStrengthCurve.FIG_8_2B, 160.0, 0.585, 0.369),
            (FatigueStrengthCurve.FIG_8_3, 160.0, 0.725, 0.561),
            (FatigueStrengthCurve.FIG_8_4, 100.0, 0.457, None),
        ],
    )
    def test_anchor_limits(self, curve: FatigueStrengthCurve, delta_sigma_c: float, d_over_c: float, l_over_c: float | None) -> None:
        """Test Δσ_D and Δσ_L against the published factors; the shear curve has no cut-off limit (None)."""
        limits = FatigueStrengthCurveLimits(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(limits.delta_sigma_d) == pytest.approx(expected=delta_sigma_c * d_over_c, rel=1e-3)

        delta_sigma_l = limits.delta_sigma_l
        if l_over_c is None:
            assert delta_sigma_l is None
        else:
            assert delta_sigma_l is not None
            assert float(delta_sigma_l) == pytest.approx(expected=delta_sigma_c * l_over_c, rel=1e-3)

    def test_fatigue_strength_factory(self) -> None:
        """Test that fatigue_strength returns the evaluator bound to this detail category and curve."""
        limits = FatigueStrengthCurveLimits(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

        strength = limits.fatigue_strength(n_cycles=2e7)

        assert isinstance(strength, Form8FatigueStrength)
        assert strength == Form8FatigueStrength(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=2e7)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        limits = FatigueStrengthCurveLimits(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)
        assert limits.label == "Figures 8.1-8.4 (fatigue strength curve limits)"
        assert limits.source_document == EN_1993_1_9_2025

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            FatigueStrengthCurveLimits(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_8_2A)
