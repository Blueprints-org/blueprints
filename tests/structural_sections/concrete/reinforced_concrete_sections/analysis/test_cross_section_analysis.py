"""Tests for CrossSectionAnalysis (caching and uncracked analysis)."""

import pytest
from shapely.errors import GEOSException

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import cross_section_analysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.cross_section_analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import StressStrainResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _analysis() -> CrossSectionAnalysis:
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


class TestUncrackedStress:
    """Tests for the uncracked analysis."""

    def test_returns_result_with_rebars(self) -> None:
        """An uncracked analysis returns an uncracked StressStrainResult with one result per rebar."""
        result = _analysis().uncracked_stress(SectionForces(n=-100, m_y=150))
        assert isinstance(result, StressStrainResult)
        assert result.is_cracked is False
        assert len(result.rebar_results) == 4


class TestCrackedStress:
    """Tests for the cracked analysis."""

    def test_returns_cracked_result_with_properties(self) -> None:
        """A cracked analysis returns a cracked result carrying the cracked properties."""
        result = _analysis().cracked_stress(SectionForces(m_y=150))
        assert result.is_cracked is True
        assert result.cracked_properties is not None
        assert result.cracked_properties.m_cr > 0
        assert len(result.rebar_results) == 4

    def test_cracked_properties_returns_properties(self) -> None:
        """cracked_properties exposes the cracking moment and a positive neutral-axis depth."""
        properties = _analysis().cracked_properties(SectionForces(m_y=150))
        assert properties.m_cr > 0
        assert properties.neutral_axis_depth > 0

    def test_cracked_stress_without_rebars_raises(self) -> None:
        """A cracked stress analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).cracked_stress(SectionForces(m_y=150))

    def test_cracked_properties_without_rebars_raises(self) -> None:
        """A cracked properties analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).cracked_properties(SectionForces(m_y=150))

    def test_non_convergence_is_wrapped_with_context(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend convergence failure is re-raised as a RuntimeError that echoes the forces."""
        analysis = _analysis()
        section = analysis._backend_section()  # noqa: SLF001 — exercising the cached backend section

        def failing_cracked_properties(*_args: object, **_kwargs: object) -> object:
            raise ValueError("could not bracket root")

        monkeypatch.setattr(section, "calculate_cracked_properties", failing_cracked_properties)
        with pytest.raises(RuntimeError, match="did not converge"):
            analysis.cracked_stress(SectionForces(m_y=150))


class TestBackendGeometryErrors:
    """Raw backend geometry failures are turned into a clear, actionable error."""

    def test_uncracked_geometry_error_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend GEOSException during the uncracked analysis becomes a clear ValueError."""
        analysis = _analysis()
        section = analysis._backend_section()  # noqa: SLF001 — exercising the cached backend section

        def failing_uncracked(*_args: object, **_kwargs: object) -> object:
            raise GEOSException("getX called on empty Point")

        monkeypatch.setattr(section, "calculate_uncracked_stress", failing_uncracked)
        with pytest.raises(ValueError, match="could not process the cross-section geometry"):
            analysis.uncracked_stress(SectionForces(m_y=100))

    def test_cracked_geometry_error_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend GEOSException during the cracked analysis becomes a clear ValueError."""
        analysis = _analysis()
        section = analysis._backend_section()  # noqa: SLF001 — exercising the cached backend section

        def failing_cracked(*_args: object, **_kwargs: object) -> object:
            raise GEOSException("getX called on empty Point")

        monkeypatch.setattr(section, "calculate_cracked_properties", failing_cracked)
        with pytest.raises(ValueError, match="could not process the cross-section geometry"):
            analysis.cracked_stress(SectionForces(m_y=150))


class TestCalculateStress:
    """Tests for the uncracked-vs-cracked regime decision."""

    def test_below_threshold_is_uncracked(self) -> None:
        """A small moment keeps the section uncracked."""
        result = _analysis().calculate_stress(SectionForces(m_y=20))
        assert result.is_cracked is False

    def test_above_threshold_is_cracked(self) -> None:
        """A large moment cracks the section."""
        result = _analysis().calculate_stress(SectionForces(m_y=150))
        assert result.is_cracked is True

    def test_compression_prevents_cracking(self) -> None:
        """A moment that cracks alone stays uncracked once enough compression is added."""
        cracks_alone = _analysis().calculate_stress(SectionForces(m_y=60))
        with_compression = _analysis().calculate_stress(SectionForces(n=-800, m_y=60))
        assert cracks_alone.is_cracked is True
        assert with_compression.is_cracked is False


class TestBiaxialBending:
    """Biaxial bending is exact when uncracked but unsupported in the cracked regime."""

    def test_uncracked_biaxial_is_supported(self) -> None:
        """An uncracked analysis accepts simultaneous m_y and m_z."""
        result = _analysis().uncracked_stress(SectionForces(m_y=20, m_z=15))
        assert result.is_cracked is False
        assert len(result.rebar_results) == 4

    def test_cracked_stress_biaxial_not_implemented(self) -> None:
        """A cracked stress analysis under biaxial bending is rejected rather than returning wrong values."""
        with pytest.raises(NotImplementedError, match="biaxial bending"):
            _analysis().cracked_stress(SectionForces(m_y=150, m_z=100))

    def test_cracked_properties_biaxial_not_implemented(self) -> None:
        """A cracked properties analysis under biaxial bending is rejected."""
        with pytest.raises(NotImplementedError, match="biaxial bending"):
            _analysis().cracked_properties(SectionForces(m_y=150, m_z=100))

    def test_calculate_stress_biaxial_that_cracks_not_implemented(self) -> None:
        """calculate_stress surfaces the biaxial limitation when the section would crack."""
        with pytest.raises(NotImplementedError, match="biaxial bending"):
            _analysis().calculate_stress(SectionForces(m_y=150, m_z=100))


class TestCaching:
    """Tests for the per-level backend section cache."""

    def test_section_built_once(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Repeated analyses reuse a single cached backend section."""
        calls = 0
        original = cross_section_analysis.build_concrete_section

        def counting_build(*args: object, **kwargs: object) -> object:
            nonlocal calls
            calls += 1
            return original(*args, **kwargs)

        monkeypatch.setattr(cross_section_analysis, "build_concrete_section", counting_build)
        analysis = _analysis()
        analysis.uncracked_stress(SectionForces(m_y=100))
        analysis.uncracked_stress(SectionForces(m_y=200))
        assert calls == 1

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
        analysis.uncracked_stress(SectionForces(m_y=100))
        analysis.invalidate_cache()
        analysis.uncracked_stress(SectionForces(m_y=100))
        assert calls == 2
