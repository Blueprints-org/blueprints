"""Testing the fatigue strength curves from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

import math

import pytest

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.figures_7 import (
    FatigueStrengthCurve,
    Fig7ConstantAmplitudeFatigueLimit,
    Fig7CutOffLimit,
    Fig7NominalStressRange,
    Fig7NumberOfCycles,
    StressType,
)
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


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


class TestFig7ConstantAmplitudeFatigueLimit:
    r"""Validation for the constant amplitude fatigue limit [$\Delta\sigma_D$] from EN 1993-1-9:2005."""

    def test_evaluation(self) -> None:
        """Test Δσ_D against the published factor of 7.1(2): Δσ_D = 0.737·Δσ_C."""
        delta_sigma_d = Fig7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert float(delta_sigma_d) == pytest.approx(expected=160.0 * 0.737, rel=1e-3)

    def test_raise_error_for_shear_curve_without_fatigue_limit(self) -> None:
        """The shear curve (Figure 7.2) has no constant amplitude fatigue limit, so the formula is undefined for it."""
        with pytest.raises(ValueError, match="no constant amplitude fatigue limit"):
            Fig7ConstantAmplitudeFatigueLimit(delta_sigma_c=100.0, curve=FatigueStrengthCurve.FIG_7_2)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_d = Fig7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert delta_sigma_d.label == "Figures 7.1-7.2 (constant amplitude fatigue limit)"
        assert delta_sigma_d.source_document == EN_1993_1_9_2005

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig7ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\Delta\sigma_{D} = \Delta\sigma_{C} \left( \frac{N_{C}}{N_{D}} \right)^{1 / m} = "
                    r"160.000 \left( \frac{2.0 \cdot 10^{6}}{5.0 \cdot 10^{6}} \right)^{1 / 3} = 117.889 \ MPa"
                ),
            ),
            ("short", r"\Delta\sigma_{D} = 117.889 \ MPa"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation, read along the first branch from the detail category."""
        latex = Fig7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestFig7CutOffLimit:
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
        delta_sigma_l = Fig7CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve)

        assert float(delta_sigma_l) == pytest.approx(expected=delta_sigma_c * l_over_c, rel=1e-3)

    def test_cut_off_over_fatigue_limit_matches_published_factor(self) -> None:
        """The direct stress cut-off limit sits 0.549 below the constant amplitude fatigue limit, per 7.1(3)."""
        curve = FatigueStrengthCurve.FIG_7_1
        delta_sigma_d = Fig7ConstantAmplitudeFatigueLimit(delta_sigma_c=160.0, curve=curve)
        delta_sigma_l = Fig7CutOffLimit(delta_sigma_c=160.0, curve=curve)

        assert float(delta_sigma_l) / float(delta_sigma_d) == pytest.approx(expected=0.549, rel=1e-3)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_l = Fig7CutOffLimit(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert delta_sigma_l.label == "Figures 7.1-7.2 (cut-off limit)"
        assert delta_sigma_l.source_document == EN_1993_1_9_2005

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig7CutOffLimit(delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                "complete",
                (
                    r"\Delta\sigma_{L} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_7_1, 160.0, "short", r"\Delta\sigma_{L} = 64.754 \ MPa"),
            (
                FatigueStrengthCurve.FIG_7_2,  # shear curve: the symbol switches from Δσ to Δτ and the reference point is C
                100.0,
                "complete",
                (
                    r"\Delta\tau_{L} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{L}} \right)^{1 / m} = "
                    r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_7_2, 100.0, "short", r"\Delta\tau_{L} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, representation: str, expected: str) -> None:
        """Test the latex representation, including the Δσ (direct) vs Δτ (shear) symbol switch."""
        latex = Fig7CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestFig7NominalStressRange:
    r"""Validation for the nominal stress range [$\Delta\sigma_R$] from EN 1993-1-9:2005."""

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
        """Test the evaluation of the nominal stress range on each branch of the curve."""
        delta_sigma_r = Fig7NominalStressRange(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles)

        assert delta_sigma_r == pytest.approx(expected=expected, rel=1e-5)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        delta_sigma_r = Fig7NominalStressRange(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1, n_cycles=1e6)

        assert delta_sigma_r.label == "Figures 7.1-7.2 (nominal stress range)"
        assert delta_sigma_r.source_document == EN_1993_1_9_2005

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig7NominalStressRange(delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_7_1, n_cycles=1e6)

    @pytest.mark.parametrize("n_cycles", [0.0, -1e6])
    def test_raise_error_if_n_cycles_not_positive(self, n_cycles: DIMENSIONLESS) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive number of cycles."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig7NominalStressRange(delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1, n_cycles=n_cycles)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "n_cycles", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                1e6,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{C} \left( \frac{N_{C}}{N} \right)^{1 / m} = "
                    r"160.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 3} = 201.587 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 1e6, "short", r"\Delta\sigma_{R} = 201.587 \ MPa"),
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                2e7,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N} \right)^{1 / m} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{2.0 \cdot 10^{7}} \right)^{1 / 5} = 89.343 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                5e8,
                "complete",
                (
                    r"\Delta\sigma_{R} = \Delta\sigma_{D} \left( \frac{N_{D}}{N_{L}} \right)^{1 / m} = "
                    r"117.889 \left( \frac{5.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 64.754 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_7_2,
                100.0,
                1e6,
                "complete",
                (
                    r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N} \right)^{1 / m} = "
                    r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{6}} \right)^{1 / 5} = 114.870 \ MPa"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_7_2,
                100.0,
                2e8,
                "complete",
                (
                    r"\Delta\tau_{R} = \Delta\tau_{C} \left( \frac{N_{C}}{N_{L}} \right)^{1 / m} = "
                    r"100.000 \left( \frac{2.0 \cdot 10^{6}}{1.0 \cdot 10^{8}} \right)^{1 / 5} = 45.731 \ MPa"
                ),
            ),
            (FatigueStrengthCurve.FIG_7_2, 100.0, 2e8, "short", r"\Delta\tau_{R} = 45.731 \ MPa"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (direct) vs Δτ (shear) symbol switch."""
        latex = Fig7NominalStressRange(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."


class TestFig7NumberOfCycles:
    r"""Validation for the number of cycles to failure [$N_R$] from EN 1993-1-9:2005."""

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
    def test_inverts_nominal_stress_range(self, curve: FatigueStrengthCurve, delta_sigma_c: float, n_cycles: float) -> None:
        """The two directions are each other's inverse: reading Δσ_R at N and feeding it back returns N."""
        delta_sigma_r = float(Fig7NominalStressRange(delta_sigma_c=delta_sigma_c, curve=curve, n_cycles=n_cycles))

        n_r = Fig7NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert n_r == pytest.approx(expected=n_cycles, rel=1e-6)

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
        n_r = Fig7NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert n_r == pytest.approx(expected=expected, rel=1e-9)

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
        n_r = Fig7NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve)

        assert math.isinf(n_r)

    def test_label_and_source_document(self) -> None:
        """Test the metadata fields."""
        n_r = Fig7NumberOfCycles(delta_sigma_r=160.0, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

        assert n_r.label == "Figures 7.1-7.2 (number of cycles)"
        assert n_r.source_document == EN_1993_1_9_2005

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
        detail = Fig7NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1).detailed_result

        assert detail["reference_point"] == expected_point
        assert detail["m"] == expected_m

    def test_detailed_result_shear_curve_anchors_at_cutoff_limit(self) -> None:
        """For the single-slope shear curve, the cut-off anchor is the cut-off limit (Δτ_L, N_L).

        Unlike the direct stress curve, the shear curve (Figure 7.2) has no constant amplitude fatigue limit: its
        single slope runs straight to the cut-off limit Δτ_L at N_L. So below Δτ_L the life is infinite and the
        detailed result reports the cut-off point itself as the governing reference (point "L", slope None).
        """
        curve = FatigueStrengthCurve.FIG_7_2
        detail = Fig7NumberOfCycles(delta_sigma_r=40.0, delta_sigma_c=100.0, curve=curve).detailed_result

        assert detail["reference_point"] == "L"
        assert detail["m"] is None
        assert detail["delta_sigma_ref"] == pytest.approx(45.730505, rel=1e-6)  # Δτ_L = 0.457·Δτ_C
        assert detail["n_ref"] == pytest.approx(curve.n_l)  # the cut-off cycle number N_L = 1e8
        assert math.isinf(detail["n_r"])

    def test_raise_error_if_negative_delta_sigma_r(self) -> None:
        """Test that a NegativeValueError is raised when the applied stress range is negative."""
        with pytest.raises(NegativeValueError):
            Fig7NumberOfCycles(delta_sigma_r=-160.0, delta_sigma_c=160.0, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize("delta_sigma_c", [0.0, -160.0])
    def test_raise_error_if_delta_sigma_c_not_positive(self, delta_sigma_c: float) -> None:
        """Test that a LessOrEqualToZeroError is raised for a non-positive detail category."""
        with pytest.raises(LessOrEqualToZeroError):
            Fig7NumberOfCycles(delta_sigma_r=160.0, delta_sigma_c=delta_sigma_c, curve=FatigueStrengthCurve.FIG_7_1)

    @pytest.mark.parametrize(
        ("curve", "delta_sigma_c", "delta_sigma_r", "representation", "expected"),
        [
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                201.587,
                "complete",
                (
                    r"N_{R} = N_{C} \left( \frac{\Delta\sigma_{C}}{\Delta\sigma_{R}} \right)^{m} = "
                    r"2.0 \cdot 10^{6} \left( \frac{160.000}{201.587} \right)^{3} = 1000005"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_7_1,
                160.0,
                89.343,
                "complete",
                (
                    r"N_{R} = N_{D} \left( \frac{\Delta\sigma_{D}}{\Delta\sigma_{R}} \right)^{m} = "
                    r"5.0 \cdot 10^{6} \left( \frac{117.889}{89.343} \right)^{5} = 20000180"
                ),
            ),
            (
                FatigueStrengthCurve.FIG_7_2,
                100.0,
                114.870,
                "complete",
                (
                    r"N_{R} = N_{C} \left( \frac{\Delta\tau_{C}}{\Delta\tau_{R}} \right)^{m} = "
                    r"2.0 \cdot 10^{6} \left( \frac{100.000}{114.870} \right)^{5} = 999993"
                ),
            ),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 201.587, "short", r"N_{R} = 1000005"),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 60.0, "complete", r"N_{R} = \infty"),
            (FatigueStrengthCurve.FIG_7_1, 160.0, 60.0, "short", r"N_{R} = \infty"),
        ],
    )
    def test_latex(self, curve: FatigueStrengthCurve, delta_sigma_c: float, delta_sigma_r: float, representation: str, expected: str) -> None:
        """Test the latex representation on each branch, including the Δσ (direct) vs Δτ (shear) symbol switch and infinite life."""
        latex = Fig7NumberOfCycles(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c, curve=curve).latex()

        actual = {"complete": latex.complete, "short": latex.short}

        assert actual[representation] == expected, f"{representation} representation failed."
