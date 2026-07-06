"""Tests for CrossSectionAnalysis (regime dispatch, creep and caching)."""

import pytest
from concreteproperties.utils import AnalysisError
from shapely.errors import GEOSException

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import cross_section_analysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import AnalysisLevel, _solve_service_curvature
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.cross_section_analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import Regime, StressStrainResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

_CONCRETE = ConcreteMaterial(ConcreteStrengthClass.C30_37)


def _analysis() -> CrossSectionAnalysis:
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


def _reference_beam_analysis() -> CrossSectionAnalysis:
    """The 300 x 600 mm C30/37 4d25 B500B reference beam of the validation page (IDEA StatiCa RCS case)."""
    cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(
        n=4, diameter=25, edge="lower", material=ReinforcementSteelMaterial(ReinforcementSteelQuality.B500B)
    )
    return CrossSectionAnalysis(cs)


def _cached_backend_section(analysis: CrossSectionAnalysis) -> object:
    """Populate and return the short-term SLS backend section (for monkeypatching its methods)."""
    return analysis._backend_section(AnalysisLevel.SLS, _CONCRETE.e_cm)  # noqa: SLF001 — exercising the cached backend section


class TestUncrackedRegime:
    """Tests for the forced uncracked regime."""

    def test_returns_result_with_rebars(self) -> None:
        """An uncracked analysis returns an SLS_UNCRACKED StressStrainResult with one result per rebar."""
        result = _analysis().stress(SectionForces(n=-100, m_y=150), regime=Regime.SLS_UNCRACKED)
        assert isinstance(result, StressStrainResult)
        assert result.regime is Regime.SLS_UNCRACKED
        assert result.is_cracked is False
        assert len(result.rebar_results) == 4


class TestCrackedRegime:
    """Tests for the forced cracked regime."""

    def test_returns_cracked_result_with_properties(self) -> None:
        """A cracked analysis returns an SLS_CRACKED result carrying the cracked properties."""
        result = _analysis().stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)
        assert result.regime is Regime.SLS_CRACKED
        assert result.is_cracked is True
        assert result.cracked_properties is not None
        assert result.cracked_properties.m_cr > 0
        assert len(result.rebar_results) == 4

    def test_cracked_without_rebars_raises(self) -> None:
        """A cracked analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)

    def test_non_convergence_is_wrapped_with_context(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend convergence failure is re-raised as a RuntimeError that echoes the forces."""
        analysis = _analysis()
        section = _cached_backend_section(analysis)

        def failing_cracked_properties(*_args: object, **_kwargs: object) -> object:
            raise ValueError("could not bracket root")

        monkeypatch.setattr(section, "calculate_cracked_properties", failing_cracked_properties)
        with pytest.raises(RuntimeError, match="did not converge"):
            analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)


class TestCrackedCombinedAxialMoment:
    """Combined N + M cracked stress: the neutral axis is solved for N and M, not the pure-bending crack depth."""

    def test_matches_hand_calculation_and_idea(self) -> None:
        """N = -300 kN, M = 200 kNm on the reference beam reproduces the closed-form / IDEA StatiCa RCS state."""
        result = _reference_beam_analysis().stress(SectionForces(n=-300, m_y=200), regime=Regime.SLS_CRACKED)
        steel_stress = max(bar.stress for bar in result.rebar_results)
        # closed-form cracked N + M solution (= IDEA StatiCa RCS): sigma_c = -17.34 MPa, sigma_s = 146.0 MPa.
        assert result.concrete_stress_min == pytest.approx(-17.34, rel=1e-2)
        assert steel_stress == pytest.approx(146.0, rel=1e-2)

    def test_neutral_axis_reflects_the_actual_state_not_the_pure_bending_crack_depth(self) -> None:
        """The strain plane carries the actual (deeper) N + M neutral axis; cracked_properties stays pure-bending."""
        analysis = _reference_beam_analysis()
        pure_bending = analysis.stress(SectionForces(m_y=200), regime=Regime.SLS_CRACKED)
        combined = analysis.stress(SectionForces(n=-300, m_y=200), regime=Regime.SLS_CRACKED)
        assert combined.cracked_properties is not None
        # cracked_properties is a pure-bending section constant: unchanged by the axial force.
        assert combined.cracked_properties.neutral_axis_depth == pytest.approx(pure_bending.cracked_properties.neutral_axis_depth, rel=1e-6)
        # the actual neutral axis under compression is deeper than that pure-bending crack depth.
        assert combined.strain_plane.neutral_axis_depth > combined.cracked_properties.neutral_axis_depth

    def test_pure_bending_is_unchanged(self) -> None:
        """With N = 0 the fast pure-bending route is used and reproduces its exact stresses."""
        result = _reference_beam_analysis().stress(SectionForces(m_y=200), regime=Regime.SLS_CRACKED)
        assert result.concrete_stress_min == pytest.approx(-16.24, rel=1e-3)
        assert max(bar.stress for bar in result.rebar_results) == pytest.approx(212.3, rel=1e-3)

    def test_sagging_and_hogging_match_on_a_symmetric_section(self) -> None:
        """On a top-bottom symmetric section a sagging and the mirrored hogging state are identical."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, edge="lower", material=ReinforcementSteelMaterial())
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, edge="upper", material=ReinforcementSteelMaterial())
        analysis = CrossSectionAnalysis(cs)
        sagging = analysis.stress(SectionForces(n=-200, m_y=140), regime=Regime.SLS_CRACKED)
        hogging = analysis.stress(SectionForces(n=-200, m_y=-140), regime=Regime.SLS_CRACKED)
        assert hogging.concrete_stress_min == pytest.approx(sagging.concrete_stress_min, rel=1e-4)
        assert max(b.stress for b in hogging.rebar_results) == pytest.approx(max(b.stress for b in sagging.rebar_results), rel=1e-4)

    def test_bending_about_either_axis_matches_on_a_square_column(self) -> None:
        """On a square 4-corner column an m_y and the equal m_z state are identical (validates the m_z route)."""
        column = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        for x in (-150, 150):
            for y in (-150, 150):
                column.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=ReinforcementSteelMaterial()))
        analysis = CrossSectionAnalysis(column)
        about_y = analysis.stress(SectionForces(n=-300, m_y=120), regime=Regime.SLS_CRACKED)
        about_z = analysis.stress(SectionForces(n=-300, m_z=120), regime=Regime.SLS_CRACKED)
        assert about_z.concrete_stress_min == pytest.approx(about_y.concrete_stress_min, rel=1e-4)
        assert max(b.stress for b in about_z.rebar_results) == pytest.approx(max(b.stress for b in about_y.rebar_results), rel=1e-4)

    def test_creep_raises_steel_stress_with_axial_force(self) -> None:
        """Creep (effective modulus) also softens the combined N + M cracked state, shedding load to the steel."""
        analysis = _reference_beam_analysis()
        forces = SectionForces(n=-300, m_y=200)
        short_term = analysis.stress(forces, regime=Regime.SLS_CRACKED)
        long_term = analysis.stress(forces, regime=Regime.SLS_CRACKED, creep_coefficient=1.0)
        assert max(b.stress for b in long_term.rebar_results) > max(b.stress for b in short_term.rebar_results)

    def test_non_convergence_is_wrapped_with_context(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend failure while solving the combined N + M state is re-raised as a clear ValueError."""
        analysis = _reference_beam_analysis()
        # trigger the SLS_CRACKED section build, then make its service-stress solve fail.
        section = analysis._backend_section(AnalysisLevel.SLS_CRACKED, _CONCRETE.e_cm)  # noqa: SLF001 — exercising the cracked backend section

        def failing_service_stress(*_args: object, **_kwargs: object) -> object:
            raise AnalysisError("could not converge on the axial force")

        monkeypatch.setattr(section, "calculate_service_stress", failing_service_stress)
        with pytest.raises(ValueError, match="did not converge"):
            analysis.stress(SectionForces(n=-300, m_y=200), regime=Regime.SLS_CRACKED)


class TestSolveServiceCurvature:
    """Unit tests for the curvature bracketing used by the combined N + M cracked solver."""

    def test_raises_when_moment_stays_below_target(self) -> None:
        """If the carried moment never reaches the target, the bracketing gives up with a clear error."""
        with pytest.raises(ValueError, match="stays below the target"):
            _solve_service_curvature(lambda _curvature: -1.0, curvature_guess=1e-6)

    def test_raises_when_moment_stays_above_target(self) -> None:
        """If the carried moment already exceeds the target everywhere, the bracketing gives up with a clear error."""
        with pytest.raises(ValueError, match="stays above the target"):
            _solve_service_curvature(lambda _curvature: 1.0, curvature_guess=1e-6)

    def test_expands_the_bracket_upward_when_the_root_exceeds_the_guess(self) -> None:
        """A root above the seed curvature makes the upper bound double outward until it straddles the root."""
        root = 10.0
        assert _solve_service_curvature(lambda curvature: curvature - root, curvature_guess=1.0) == pytest.approx(root)

    def test_shrinks_the_bracket_downward_when_the_root_is_below_the_guess(self) -> None:
        """A root well below the seed curvature makes the lower bound halve inward until it straddles the root."""
        root = 1e-9
        assert _solve_service_curvature(lambda curvature: curvature - root, curvature_guess=1e-3) == pytest.approx(root)


class TestUlsRegime:
    """Tests for the ULS stress/strain analysis at a design action."""

    def test_returns_uls_result_with_design_stress_block(self) -> None:
        """The ULS state pivots on concrete crushing: extreme fibre at -f_cd, steel yielding at f_yd."""
        result = _analysis().stress(SectionForces(m_y=150), regime=Regime.ULS)
        assert result.regime is Regime.ULS
        assert result.is_cracked is False
        assert result.concrete_stress_min == pytest.approx(-_CONCRETE.f_cd, rel=1e-3)
        steel = ReinforcementSteelMaterial()
        assert result.rebar_results[0].stress == pytest.approx(steel.f_yd, rel=1e-3)

    def test_strain_plane_comes_from_the_pivot_geometry(self) -> None:
        """The ULS strain plane pivots at eps_cu3 on the compression fibre with the capacity's NA depth."""
        analysis = _analysis()
        result = analysis.stress(SectionForces(m_y=150), regime=Regime.ULS)
        plane = result.strain_plane
        assert plane is not None
        assert plane.strain_at(0, 250) == pytest.approx(-_CONCRETE.eps_cu3, rel=1e-6)
        assert plane.neutral_axis_depth == pytest.approx(analysis.bending_capacity().neutral_axis_depth, rel=1e-6)
        assert plane.neutral_axis_angle == pytest.approx(0.0)

    def test_strain_plane_matches_rebar_strains(self) -> None:
        """The pivot-based plane reproduces the backend's own rebar strains (never stress / E)."""
        result = _analysis().stress(SectionForces(m_y=150), regime=Regime.ULS)
        plane = result.strain_plane
        assert plane is not None
        for rebar in result.rebar_results:
            assert plane.strain_at(rebar.x, rebar.y) == pytest.approx(rebar.strain, rel=1e-4, abs=1e-6)

    def test_hogging_flips_the_pivot_to_the_bottom(self) -> None:
        """A hogging design action pivots on the bottom fibre instead."""
        result = _analysis().stress(SectionForces(m_y=-150), regime=Regime.ULS)
        plane = result.strain_plane
        assert plane is not None
        assert plane.strain_at(0, -250) == pytest.approx(-_CONCRETE.eps_cu3, rel=1e-6)
        assert plane.strain_at(0, 250) > 0

    def test_creep_coefficient_is_ignored_at_uls(self) -> None:
        """The ULS analysis uses design materials; the creep coefficient does not change the result."""
        short_term = _analysis().stress(SectionForces(m_y=150), regime=Regime.ULS)
        with_creep = _analysis().stress(SectionForces(m_y=150), regime=Regime.ULS, creep_coefficient=2.0)
        assert with_creep.concrete_stress_min == short_term.concrete_stress_min
        assert with_creep.rebar_results[0].stress == short_term.rebar_results[0].stress

    def test_uls_without_rebars_raises(self) -> None:
        """A ULS stress analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Ultimate stress analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).stress(SectionForces(m_y=150), regime=Regime.ULS)


class TestBackendGeometryErrors:
    """Raw backend geometry failures are turned into a clear, actionable error."""

    def test_uncracked_geometry_error_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend GEOSException during the uncracked analysis becomes a clear ValueError."""
        analysis = _analysis()
        section = _cached_backend_section(analysis)

        def failing_uncracked(*_args: object, **_kwargs: object) -> object:
            raise GEOSException("getX called on empty Point")

        monkeypatch.setattr(section, "calculate_uncracked_stress", failing_uncracked)
        with pytest.raises(ValueError, match="could not process the cross-section geometry"):
            analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED)

    def test_cracked_geometry_error_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend GEOSException during the cracked analysis becomes a clear ValueError."""
        analysis = _analysis()
        section = _cached_backend_section(analysis)

        def failing_cracked(*_args: object, **_kwargs: object) -> object:
            raise GEOSException("getX called on empty Point")

        monkeypatch.setattr(section, "calculate_cracked_properties", failing_cracked)
        with pytest.raises(ValueError, match="could not process the cross-section geometry"):
            analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)


class TestAutoRegime:
    """Tests for the automatic uncracked-vs-cracked decision."""

    def test_below_threshold_is_uncracked(self) -> None:
        """A small moment keeps the section uncracked."""
        result = _analysis().stress(SectionForces(m_y=20))
        assert result.regime is Regime.SLS_UNCRACKED

    def test_above_threshold_is_cracked(self) -> None:
        """A large moment cracks the section."""
        result = _analysis().stress(SectionForces(m_y=150))
        assert result.regime is Regime.SLS_CRACKED

    def test_compression_prevents_cracking(self) -> None:
        """A moment that cracks alone stays uncracked once enough compression is added."""
        cracks_alone = _analysis().stress(SectionForces(m_y=60))
        with_compression = _analysis().stress(SectionForces(n=-800, m_y=60))
        assert cracks_alone.regime is Regime.SLS_CRACKED
        assert with_compression.regime is Regime.SLS_UNCRACKED

    def test_auto_cracking_without_rebars_raises(self) -> None:
        """AUTO surfaces the missing-reinforcement error when the section would crack."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).stress(SectionForces(m_y=150))


class TestCreep:
    """Tests for the creep coefficient (effective modulus E_c,eff = E_cm / (1 + phi))."""

    def test_negative_creep_coefficient_raises(self) -> None:
        """A negative creep coefficient is rejected."""
        with pytest.raises(ValueError, match="creep coefficient"):
            _analysis().stress(SectionForces(m_y=150), creep_coefficient=-0.5)

    def test_zero_creep_equals_default(self) -> None:
        """creep_coefficient=0.0 reproduces the short-term result exactly."""
        forces = SectionForces(n=-100, m_y=150)
        default = _analysis().stress(forces)
        short_term = _analysis().stress(forces, creep_coefficient=0.0)
        assert short_term.concrete_stress_min == default.concrete_stress_min
        assert short_term.rebar_results[0].stress == default.rebar_results[0].stress

    def test_creep_raises_steel_stress_in_cracked_regime(self) -> None:
        """A softer concrete (creep) sheds load to the reinforcement: the steel stress goes up."""
        forces = SectionForces(m_y=150)
        short_term = _analysis().stress(forces, regime=Regime.SLS_CRACKED)
        long_term = _analysis().stress(forces, regime=Regime.SLS_CRACKED, creep_coefficient=2.0)
        assert long_term.rebar_results[0].stress > short_term.rebar_results[0].stress

    def test_creep_deepens_the_cracked_neutral_axis(self) -> None:
        """A higher modular ratio (creep) deepens the cracked neutral axis."""
        forces = SectionForces(m_y=150)
        short_term = _analysis().stress(forces, regime=Regime.SLS_CRACKED)
        long_term = _analysis().stress(forces, regime=Regime.SLS_CRACKED, creep_coefficient=2.0)
        assert short_term.cracked_properties is not None
        assert long_term.cracked_properties is not None
        assert long_term.cracked_properties.neutral_axis_depth > short_term.cracked_properties.neutral_axis_depth

    def test_result_carries_the_effective_modulus(self) -> None:
        """The result's elastic modulus is E_cm / (1 + phi)."""
        result = _analysis().stress(SectionForces(m_y=20), creep_coefficient=1.0)
        assert result.elastic_modulus == pytest.approx(_CONCRETE.e_cm / 2.0)


class TestBiaxialBending:
    """Biaxial bending is exact when uncracked but unsupported in the cracked regime."""

    def test_uncracked_biaxial_is_supported(self) -> None:
        """An uncracked analysis accepts simultaneous m_y and m_z."""
        result = _analysis().stress(SectionForces(m_y=20, m_z=15), regime=Regime.SLS_UNCRACKED)
        assert result.regime is Regime.SLS_UNCRACKED
        assert len(result.rebar_results) == 4

    def test_cracked_biaxial_not_implemented(self) -> None:
        """A cracked analysis under biaxial bending is rejected rather than returning wrong values."""
        with pytest.raises(NotImplementedError, match="biaxial bending"):
            _analysis().stress(SectionForces(m_y=150, m_z=100), regime=Regime.SLS_CRACKED)

    def test_auto_biaxial_that_cracks_not_implemented(self) -> None:
        """AUTO surfaces the biaxial limitation when the section would crack."""
        with pytest.raises(NotImplementedError, match="biaxial bending"):
            _analysis().stress(SectionForces(m_y=150, m_z=100))


class TestCaching:
    """Tests for the per-configuration backend section cache."""

    def test_section_built_once(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Repeated analyses with the same configuration reuse a single cached backend section."""
        calls = 0
        original = cross_section_analysis.build_concrete_section

        def counting_build(*args: object, **kwargs: object) -> object:
            nonlocal calls
            calls += 1
            return original(*args, **kwargs)

        monkeypatch.setattr(cross_section_analysis, "build_concrete_section", counting_build)
        analysis = _analysis()
        analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED)
        analysis.stress(SectionForces(m_y=200), regime=Regime.SLS_UNCRACKED)
        assert calls == 1

    def test_different_creep_coefficients_build_separate_sections(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Creep changes the effective modulus, so each creep coefficient gets its own backend section."""
        calls = 0
        original = cross_section_analysis.build_concrete_section

        def counting_build(*args: object, **kwargs: object) -> object:
            nonlocal calls
            calls += 1
            return original(*args, **kwargs)

        monkeypatch.setattr(cross_section_analysis, "build_concrete_section", counting_build)
        analysis = _analysis()
        analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED)
        analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED, creep_coefficient=2.0)
        analysis.stress(SectionForces(m_y=200), regime=Regime.SLS_UNCRACKED, creep_coefficient=2.0)
        assert calls == 2

    def test_invalidate_cache_forces_rebuild(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """invalidate_cache drops the cached section so the next analysis rebuilds it."""
        calls = 0
        original = cross_section_analysis.build_concrete_section

        def counting_build(*args: object, **kwargs: object) -> object:
            nonlocal calls
            calls += 1
            return original(*args, **kwargs)

        monkeypatch.setattr(cross_section_analysis, "build_concrete_section", counting_build)
        analysis = _analysis()
        analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED)
        analysis.invalidate_cache()
        analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED)
        assert calls == 2
