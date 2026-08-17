"""Testing the fatigue strength curve limits from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve_limits import (
    Form7ConstantAmplitudeFatigueLimit,
    Form7CutOffLimit,
    form7_curve_corner_points,
)
from blueprints.validations import NegativeValueError


class TestForm7ConstantAmplitudeFatigueLimit:
    r"""Validation for the constant amplitude fatigue limit [$\Delta\sigma_D$] from EN 1993-1-9:2005."""

    def test_evaluation(self) -> None:
        """Test Δσ_D against the published factor of 7.1(2): Δσ_D = 0.737·Δσ_C."""
        delta_sigma_d = Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert float(delta_sigma_d) == pytest.approx(expected=160.0 * 0.737, rel=1e-3)

    def test_raise_error_for_shear_curve_without_fatigue_limit(self) -> None:
        """The shear curve (Figure 7.2) has no constant amplitude fatigue limit, so the formula is undefined for it."""
        with pytest.raises(ValueError, match="no constant amplitude fatigue limit"):
            Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=100.0, curve=FatigueStrengthCurve.FIG_7_2)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_d = Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert delta_sigma_d.label == "Figures 7.1-7.2 (constant amplitude fatigue limit)"
        assert delta_sigma_d.source_document == EN_1993_1_9_2005

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\Delta\sigma_{D} = \Delta\sigma_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m} = "
                r"160.000 \left( \frac{2.0 \cdot 10^{6}}{5.0 \cdot 10^{6}} \right)^{1 / 3} = 117.889 \ MPa",
            ),
            ("short", r"\Delta\sigma_{D} = 117.889 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation, delegated to the underlying curve-value relation."""
        latex = Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm7CutOffLimit:
    r"""Validation for the cut-off limit [$\Delta\sigma_L$] from EN 1993-1-9:2005."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "l_over_c"),
        [
            (FatigueStrengthCurve.FIG_7_1, 160.0, 0.405),  # Δσ_L = 0.549·Δσ_D = 0.549·0.737·Δσ_C
            (FatigueStrengthCurve.FIG_7_2, 100.0, 0.457),  # Δτ_L = 0.457·Δτ_C
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, l_over_c: float) -> None:
        """Test Δσ_L (and Δτ_L) against the published factors of 7.1(2) and 7.1(3)."""
        delta_sigma_l = Form7CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(delta_sigma_l) == pytest.approx(expected=delta_sigma_c * l_over_c, rel=1e-3)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_l = Form7CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert delta_sigma_l.label == "Figures 7.1-7.2 (cut-off limit)"
        assert delta_sigma_l.source_document == EN_1993_1_9_2005

    def test_raise_error_if_negative_delta_sigma_c(self) -> None:
        """Test that a NegativeValueError is raised when delta_sigma_c is negative."""
        with pytest.raises(NegativeValueError):
            Form7CutOffLimit(delta_sigma_c=-160.0, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                "complete",
                r"\Delta\sigma_{L} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m} = "
                r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_7_1, 160.0, "short", r"\Delta\sigma_{L} = 64.754 \ MPa"),
            (
                FatigueStrengthCurve.FIG_7_2,  # shear curve: the symbol switches from Δσ to Δτ and the reference point is C
                100.0,
                "complete",
                r"\Delta\tau_{L} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{L}} \right)^{1 / m} = "
                r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa",
            ),
            (FatigueStrengthCurve.FIG_7_2, 100.0, "short", r"\Delta\tau_{L} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, representation: str, expected: str) -> None:
        """Test the latex representation, including the Δσ (direct) vs Δτ (shear) symbol switch."""
        latex = Form7CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestForm7CurveCornerPoints:
    """Validation for the corner points C (, D), L of an EN 1993-1-9:2005 fatigue strength curve."""

    def test_direct_stress_curve_returns_c_d_l(self) -> None:
        """The direct stress curve (Figure 7.1) returns C, D and L in order of increasing cycles."""
        points = form7_curve_corner_points(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert [point.point for point in points] == ["C", "D", "L"]
        assert [point.n_cycles for point in points] == [2e6, 5e6, 1e8]
        assert points[0].delta_sigma == pytest.approx(160.0)
        assert points[1].delta_sigma == pytest.approx(
            float(Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1))
        )
        assert points[2].delta_sigma == pytest.approx(float(Form7CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)))

    def test_shear_curve_returns_c_l_without_d(self) -> None:
        """The single-slope shear curve (Figure 7.2) runs straight to its cut-off, so it returns only C and L."""
        points = form7_curve_corner_points(delta_sigma_c=100.0, curve=FatigueStrengthCurve.FIG_7_2)

        assert [point.point for point in points] == ["C", "L"]
        assert [point.n_cycles for point in points] == [2e6, 1e8]
        assert points[0].delta_sigma == pytest.approx(100.0)
        assert points[1].delta_sigma == pytest.approx(float(Form7CutOffLimit(delta_sigma_c=100.0, curve=FatigueStrengthCurve.FIG_7_2)))
