"""Testing the fatigue strength curve limits from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_limits import (
    Form8ConstantAmplitudeFatigueLimit,
    Form8CutOffLimit,
)
from blueprints.validations import NegativeValueError


class TestForm8ConstantAmplitudeFatigueLimit:
    r"""Validation for the constant amplitude fatigue limit [$\Delta\sigma_D$] from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "d_over_c"),
        [
            (FatigueStrengthCurve.FIG_8_1A, 160.0, 1.000),
            (FatigueStrengthCurve.FIG_8_1B, 160.0, 1.000),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 0.737),
            (FatigueStrengthCurve.FIG_8_2B, 160.0, 0.585),
            (FatigueStrengthCurve.FIG_8_3, 160.0, 0.725),
            (FatigueStrengthCurve.FIG_8_4, 100.0, 0.457),  # shear curve: the shear fatigue limit Δτ_D
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, d_over_c: float) -> None:
        """Test Δσ_D against the published factors, including the shear curve (Δτ_D)."""
        delta_sigma_d = Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(delta_sigma_d) == pytest.approx(expected=delta_sigma_c * d_over_c, rel=1e-3)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_d = Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

        assert delta_sigma_d.label == "Figures 8.1-8.4 (constant amplitude fatigue limit)"
        assert delta_sigma_d.source_document == EN_1993_1_9_2025

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_8_2A)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                "complete",
                r"\Delta\sigma_{D} = \Delta\sigma_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                r"160.000 \left( \frac{2.0 \cdot 10^{6}}{5.0 \cdot 10^{6}} \right)^{1 / 3} = 117.889 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, "short", r"\Delta\sigma_{D} = 117.889 \ MPa"),
            (
                FatigueStrengthCurve.FIG_8_4,  # shear curve: the symbol switches from Δσ to Δτ
                100.0,
                "complete",
                r"\Delta\tau_{D} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_8_4, 100.0, "short", r"\Delta\tau_{D} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, representation: str, expected: str) -> None:
        """Test the latex representation, including the Δσ (normal) vs Δτ (shear) symbol switch."""
        latex = Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm8CutOffLimit:
    r"""Validation for the cut-off limit [$\Delta\sigma_L$] from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "l_over_c"),
        [
            (FatigueStrengthCurve.FIG_8_1A, 160.0, 0.647),
            (FatigueStrengthCurve.FIG_8_1B, 160.0, 0.457),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 0.405),
            (FatigueStrengthCurve.FIG_8_2B, 160.0, 0.369),
            (FatigueStrengthCurve.FIG_8_3, 160.0, 0.561),
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, l_over_c: float) -> None:
        """Test Δσ_L against the published factors for the curves that have a separate cut-off branch."""
        delta_sigma_l = Form8CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(delta_sigma_l) == pytest.approx(expected=delta_sigma_c * l_over_c, rel=1e-3)

    def test_raise_error_for_shear_curve_without_cutoff(self) -> None:
        """The shear curve (Figure 8.4) has no separate cut-off branch, so the cut-off limit is undefined."""
        with pytest.raises(ValueError, match="no separate cut-off limit"):
            Form8CutOffLimit(delta_sigma_c=100.0, curve=FatigueStrengthCurve.FIG_8_4)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_l = Form8CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

        assert delta_sigma_l.label == "Figures 8.1-8.4 (cut-off limit)"
        assert delta_sigma_l.source_document == EN_1993_1_9_2025

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            Form8CutOffLimit(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_8_2A)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta\sigma_{L} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m_{2}} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa",
            ),
            ("short", r"\Delta\sigma_{L} = 64.754 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation, delegated to the underlying curve-value relation."""
        latex = Form8CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
