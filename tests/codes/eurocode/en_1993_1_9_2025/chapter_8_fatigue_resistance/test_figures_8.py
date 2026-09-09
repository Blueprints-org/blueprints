"""Testing the fatigue strength curves from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

import math

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.figures_8 import (
    FatigueStrengthCurve,
    Fig8ConstantAmplitudeFatigueLimit,
    Fig8CutOffLimit,
    Fig8NominalStressRange,
    Fig8NumberOfCycles,
    StressType,
)
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


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


class TestFig8ConstantAmplitudeFatigueLimit:
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
        """Test Δσ_D against the published factors of Figures 8.1 - 8.4, including the shear curve (Δτ_D)."""
        delta_sigma_d = Fig8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(delta_sigma_d) == pytest.approx(expected=delta_sigma_c * d_over_c, rel=1e-3)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_d = Fig8ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

        assert delta_sigma_d.label == "Figures 8.1-8.4 (constant amplitude fatigue limit)"
        assert delta_sigma_d.source_document == EN_1993_1_9_2025

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_8_2A)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                "complete",
                (
                    r"\Delta\sigma_{D} = \Delta\sigma_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                    r"160.000 \left( \frac{2.0 \cdot 10^{6}}{5.0 \cdot 10^{6}} \right)^{1 / 3} = 117.889 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, "short", r"\Delta\sigma_{D} = 117.889 \ MPa"),
            (
                FatigueStrengthCurve.FIG_8_4,  # shear curve: the symbol switches from Δσ to Δτ
                100.0,
                "complete",
                (
                    r"\Delta\tau_{D} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                    r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_8_4, 100.0, "short", r"\Delta\tau_{D} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, representation: str, expected: str) -> None:
        """Test the latex representation, including the Δσ (normal) vs Δτ (shear) symbol switch."""
        latex = Fig8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestFig8CutOffLimit:
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
        delta_sigma_l = Fig8CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(delta_sigma_l) == pytest.approx(expected=delta_sigma_c * l_over_c, rel=1e-3)

    def test_raise_error_for_shear_curve_without_cutoff(self) -> None:
        """The shear curve (Figure 8.4) has no separate cut-off branch, so the cut-off limit is undefined."""
        with pytest.raises(ValueError, match="no separate cut-off limit"):
            Fig8CutOffLimit(delta_sigma_c=100.0, curve=FatigueStrengthCurve.FIG_8_4)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_l = Fig8CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

        assert delta_sigma_l.label == "Figures 8.1-8.4 (cut-off limit)"
        assert delta_sigma_l.source_document == EN_1993_1_9_2025

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig8CutOffLimit(delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_8_2A)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\Delta\sigma_{L} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m_{2}} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa"
                ),
            ),
            ("short", r"\Delta\sigma_{L} = 64.754 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation, read along the second branch from the constant amplitude fatigue limit."""
        latex = Fig8CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestFig8NominalStressRange:
    r"""Validation for the nominal stress range [$\Delta\sigma_R$] from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "expected"),
        [
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e6, 201.58737),  # first branch (slope m1), N < N_D
            (FatigueStrengthCurve.FIG_8_1B, 160.0, 2e6, 160.00000),  # N_C = N_D boundary -> Δσ_D = Δσ_C
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 5e6, 117.88901),  # N_D boundary -> Δσ_D
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 2e7, 89.34316),  # second branch (slope m2), N_D < N < N_L
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e8, 64.75411),  # N_L boundary -> Δσ_L
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 5e8, 64.75411),  # cut-off, N > N_L -> Δσ_L (constant)
            (FatigueStrengthCurve.FIG_8_1A, 160.0, 1e8, 103.59661),  # slope m2 = 9, N_L boundary -> Δσ_L = 0.647·Δσ_C
            (FatigueStrengthCurve.FIG_8_2B, 160.0, 1e8, 59.03777),  # N_D = 1e7, second branch down to Δσ_L = 0.369·Δσ_C
            (FatigueStrengthCurve.FIG_8_3, 160.0, 1e8, 89.78729),  # slope m1 = 5, m2 = 9 -> Δσ_L = 0.561·Δσ_C
            (FatigueStrengthCurve.FIG_8_4, 100.0, 1e6, 114.86984),  # shear, first branch
            (FatigueStrengthCurve.FIG_8_4, 100.0, 2e8, 45.73051),  # shear, beyond N_D -> Δτ_D (constant)
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, expected: float) -> None:
        """Test the evaluation of the nominal stress range on each branch of the curve."""
        delta_sigma_r = Fig8NominalStressRange(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles)

        assert delta_sigma_r == pytest.approx(expected=expected, rel=1e-5)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_r = Fig8NominalStressRange(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=1e6)

        assert delta_sigma_r.label == "Figures 8.1-8.4 (nominal stress range)"
        assert delta_sigma_r.source_document == EN_1993_1_9_2025

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig8NominalStressRange(delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=1e6)

    @pytest.mark.parametrize("n_cycles", [0.0, -1e6])
    def test_raise_error_if_n_cycles_not_positive(self, n_cycles: DIMENSIONLESS) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive number of cycles."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig8NominalStressRange(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=n_cycles)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                1e6,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{C} \left( \frac{N_{C}}{N} \right)^{1 / m_{1}} = "
                    r"160.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 3} = 201.587 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e6, "short", r"\Delta\sigma_{R} = 201.587 \ MPa"),
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                2e7,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N} \right)^{1 / m_{2}} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{2.0 \cdot 10^{7}} \right)^{1 / 5} = 89.343 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                5e8,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m_{2}} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_8_4,
                100.0,
                1e6,
                "complete",
                (
                    r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N} \right)^{1 / m_{1}} = "
                    r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 5} = 114.870 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_8_4,
                100.0,
                2e8,
                "complete",
                (
                    r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m_{1}} = "
                    r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_8_4, 100.0, 2e8, "short", r"\Delta\tau_{R} = 45.731 \ MPa"),
            (
                FatigueStrengthCurve.FIG_8_2A,  # exactly at N_L the target is still rendered as N, not N_L
                160.0,
                1e8,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N} \right)^{1 / m_{2}} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_8_1A,  # the only curves with a slope of 9 are Figures 8.1a and 8.3
                160.0,
                1e8,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N} \right)^{1 / m_{2}} = "
                    r"160.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 9} = 103.597 \ MPa"
                ),
            ),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (normal) vs Δτ (shear) symbol switch."""
        latex = Fig8NominalStressRange(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."

    def test_latex_without_decimals(self) -> None:
        """At n = 0 the stress values lose their decimals and the integer slope is rendered without a decimal point."""
        latex = Fig8NominalStressRange(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A, n_cycles=1e6).latex(n=0)

        assert latex.complete == (
            r"\Delta\sigma_{R} = \Delta\sigma_{C} \left( \frac{N_{C}}{N} \right)^{1 / m_{1}} = "
            r"160 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 3} = 202 \ MPa"
        )


class TestFig8NumberOfCycles:
    r"""Validation for the number of cycles to failure [$N_R$] from EN 1993-1-9:2025."""

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles"),
        [
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e6),  # first branch (slope m1), N < N_D
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 5e6),  # N_D boundary -> Δσ_D maps back to N_D
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 2e7),  # second branch (slope m2), N_D < N < N_L
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 1e8),  # N_L boundary -> Δσ_L maps back to N_L
            (FatigueStrengthCurve.FIG_8_1B, 160.0, 3e6),  # other normal curve, second branch
            (FatigueStrengthCurve.FIG_8_4, 100.0, 1e6),  # shear, single slope
            (FatigueStrengthCurve.FIG_8_4, 100.0, 1e8),  # shear, N_D boundary -> Δτ_D maps back to N_D
        ],
    )
    def test_inverts_nominal_stress_range(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float) -> None:
        """The two directions are each other's inverse: reading Δσ_R at N and feeding it back returns N."""
        delta_sigma_r = float(Fig8NominalStressRange(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles))

        n_r = Fig8NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert n_r == pytest.approx(expected=n_cycles, rel=1e-6)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r", "expected"),
        [
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 160.0, 2e6),  # Δσ_R = Δσ_C maps to the reference point N_C
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 320.0, 2e6 / 8),  # halving the life-cube: N_R = N_C (Δσ_C/Δσ_R)^3
            (FatigueStrengthCurve.FIG_8_4, 100.0, 100.0, 2e6),  # shear, Δτ_R = Δτ_C maps to N_C
        ],
    )
    def test_evaluation(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float, expected: float) -> None:
        """Test the evaluation against directly computed reference points."""
        n_r = Fig8NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert n_r == pytest.approx(expected=expected, rel=1e-9)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r"),
        [
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 60.0),  # below the cut-off limit Δσ_L = 64.75
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 0.0),  # a zero stress range never accumulates damage
            (FatigueStrengthCurve.FIG_8_4, 100.0, 40.0),  # shear, below the fatigue limit Δτ_D = 45.73
        ],
    )
    def test_infinite_life_below_cutoff(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float) -> None:
        """Below the cut-off limit (or below Δτ_D for shear) the life is infinite, i.e. no fatigue damage."""
        n_r = Fig8NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert math.isinf(n_r)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        n_r = Fig8NumberOfCycles(delta_sigma_r=160.0, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

        assert n_r.label == "Figures 8.1-8.4 (number of cycles)"
        assert n_r.source_document == EN_1993_1_9_2025

    @pytest.mark.parametrize(
        ("delta_sigma_r", "expected_point", "expected_m", "expected_delta_sigma_ref", "expected_n_ref"),
        [
            (201.587, "C", 3.0, 160.0, 2e6),  # first branch, anchored at the detail category
            (89.343, "D", 5.0, 117.889, 5e6),  # second branch, anchored at the constant amplitude fatigue limit
            (60.0, "L", None, 64.754, 1e8),  # below the cut-off limit, anchored at the cut-off point
        ],
    )
    def test_detailed_result_reports_governing_branch(
        self,
        delta_sigma_r: float,
        expected_point: str,
        expected_m: float | None,
        expected_delta_sigma_ref: float,
        expected_n_ref: float,
    ) -> None:
        """The detailed result exposes the whole governing anchor, so callers can label N_R without re-deriving it."""
        n_r = Fig8NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)
        detail = n_r.detailed_result

        assert detail["reference_point"] == expected_point
        assert detail["m"] == expected_m
        assert detail["delta_sigma_ref"] == pytest.approx(expected_delta_sigma_ref, rel=1e-4)
        assert detail["n_ref"] == pytest.approx(expected_n_ref)
        assert detail["n_r"] == float(n_r)

    def test_stress_range_read_beyond_the_cut_off_maps_back_to_n_l(self) -> None:
        """Past N_L the curve is flat, so the two directions stop being inverses: any N > N_L reads Δσ_L, which maps back to N_L."""
        curve = FatigueStrengthCurve.FIG_8_2A
        delta_sigma_l = float(Fig8NominalStressRange(delta_sigma_c=160.0, curve=curve, n_cycles=5e8))

        n_r = Fig8NumberOfCycles(delta_sigma_r=delta_sigma_l, delta_sigma_c=160.0, curve=curve)

        assert n_r == pytest.approx(expected=curve.n_l, rel=1e-9)

    def test_detailed_result_shear_curve_anchors_at_fatigue_limit_below_cutoff(self) -> None:
        """For the single-slope shear curve, the cut-off anchor is the constant amplitude fatigue limit (Δτ_D, N_D).

        Unlike a normal curve, the shear curve (Figure 8.4) has no separate cut-off limit Δτ_L: its fatigue limit
        Δτ_D doubles as the cut-off. So below Δτ_D the life is infinite and the detailed result reports the fatigue
        limit point itself as the governing reference (point "L", slope None, N_ref = N_D rather than N_L).
        """
        curve = FatigueStrengthCurve.FIG_8_4
        detail = Fig8NumberOfCycles(delta_sigma_r=40.0, delta_sigma_c=100.0, curve=curve).detailed_result

        assert detail["reference_point"] == "L"
        assert detail["m"] is None
        assert detail["delta_sigma_ref"] == pytest.approx(45.730505, rel=1e-6)  # Δτ_D, doubling as the cut-off
        assert detail["n_ref"] == pytest.approx(curve.n_d)  # the fatigue limit cycle number N_D = 1e8, not a separate N_L
        assert math.isinf(detail["n_r"])

    def test_detailed_result_normal_curve_anchors_at_cutoff_limit(self) -> None:
        """For a two-branch curve the cut-off anchor is the cut-off limit itself (Δσ_L, N_L)."""
        curve = FatigueStrengthCurve.FIG_8_2A
        detail = Fig8NumberOfCycles(delta_sigma_r=60.0, delta_sigma_c=160.0, curve=curve).detailed_result

        assert detail["delta_sigma_ref"] == pytest.approx(64.754, rel=1e-4)
        assert detail["n_ref"] == pytest.approx(curve.n_l)

    def test_raise_error_if_negative_delta_sigma_r(self) -> None:
        """Test that a NegativeValueError is raised when the applied stress range is negative."""
        with pytest.raises(NegativeValueError):
            Fig8NumberOfCycles(delta_sigma_r=-160.0, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_8_2A)

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig8NumberOfCycles(delta_sigma_r=160.0, delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_8_2A)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                201.587,
                "complete",
                (
                    r"N_{R} = N_{C} \left( \frac{\Delta\sigma_{C}}{\Delta\sigma_{R}} \right)^{m_{1}} = "
                    r"2.0 \cdot 10^{6} \left( \frac{160.000}{201.587} \right)^{3} = 1000005"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_8_2A,
                160.0,
                89.343,
                "complete",
                (
                    r"N_{R} = N_{D} \left( \frac{\Delta\sigma_{D}}{\Delta\sigma_{R}} \right)^{m_{2}} = "
                    r"5.0 \cdot 10^{6} \left( \frac{117.889}{89.343} \right)^{5} = 20000180"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_8_4,
                100.0,
                114.870,
                "complete",
                (
                    r"N_{R} = N_{C} \left( \frac{\Delta\tau_{C}}{\Delta\tau_{R}} \right)^{m_{1}} = "
                    r"2.0 \cdot 10^{6} \left( \frac{100.000}{114.870} \right)^{5} = 999993"
                ),
            ),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 201.587, "short", r"N_{R} = 1000005"),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 60.0, "complete", r"N_{R} = \infty"),
            (FatigueStrengthCurve.FIG_8_2A, 160.0, 60.0, "short", r"N_{R} = \infty"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (normal) vs Δτ (shear) symbol switch and infinite life."""
        latex = Fig8NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
