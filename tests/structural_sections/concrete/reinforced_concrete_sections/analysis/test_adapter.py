"""Tests for the concreteproperties adapter (material mapping and section building)."""

import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass, DiagramType
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    _MESH_GUARD_FLAG,
    AnalysisLevel,
    SteelBranch,
    _deduplicate_pslg,
    _guard_degenerate_meshes,
    _service_steel,
    _ultimate_profile,
    _ultimate_steel,
    backend_analysis_section,
    build_concrete_section,
    effective_modulus,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import (
    RectangularReinforcedCrossSection,
)
from blueprints.unit_conversion import PER_MILLE_TO_RATIO


def _section(concrete_material: ConcreteMaterial | None = None) -> RectangularReinforcedCrossSection:
    """Build a 300x500 reinforced section with 4 D20 on the lower edge."""
    cs = RectangularReinforcedCrossSection(
        width=300,
        height=500,
        concrete_material=concrete_material or ConcreteMaterial(ConcreteStrengthClass.C30_37),
    )
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return cs


class TestBuildConcreteSection:
    """Tests for build_concrete_section."""

    def test_maps_concrete_service_modulus(self) -> None:
        """The concrete service profile carries the secant modulus e_cm by default."""
        section = build_concrete_section(_section())
        concrete_material = section.concrete_geometries[0].material
        assert concrete_material.stress_strain_profile.elastic_modulus == ConcreteMaterial(ConcreteStrengthClass.C30_37).e_cm

    def test_explicit_elastic_modulus_overrides_service_modulus(self) -> None:
        """An explicit (effective) elastic modulus replaces e_cm in the service profile."""
        section = build_concrete_section(_section(), elastic_modulus=16000.0)
        assert section.concrete_geometries[0].material.stress_strain_profile.elastic_modulus == 16000.0

    def test_flexural_tensile_strength_from_formula_3_23(self) -> None:
        """flexural_tensile_strength = f_ctm,fl for the 500 mm member height: (1.6 - 500/1000) * f_ctm."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        section = build_concrete_section(_section())
        assert section.concrete_geometries[0].material.flexural_tensile_strength == pytest.approx((1.6 - 500 / 1000) * concrete.f_ctm)

    def test_adds_one_lumped_bar_per_rebar(self) -> None:
        """Each longitudinal rebar becomes one lumped reinforcement bar."""
        section = build_concrete_section(_section())
        assert len(section.reinf_geometries_lumped) == 4

    def test_uls_level_maps_design_concrete(self) -> None:
        """The ULS concrete curve is bilinear-horizontal at f_cd up to eps_cu3, with a tension branch."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        section = build_concrete_section(_section(), level=AnalysisLevel.ULS)
        profile = section.concrete_geometries[0].material.stress_strain_profile
        assert max(profile.stresses) == pytest.approx(concrete.f_cd)
        assert profile.ultimate_strain == pytest.approx(concrete.eps_cu3 * PER_MILLE_TO_RATIO)
        # tension branch peaks at f_ctm,fl for the 500 mm member height (backend tension negative)
        assert min(profile.stresses) == pytest.approx(-(1.6 - 500 / 1000) * concrete.f_ctm)
        # the compression elbow sits at f_cd / e_cm (linear at the secant modulus)
        assert profile.get_stress(0.5 * concrete.f_cd / concrete.e_cm) == pytest.approx(0.5 * concrete.f_cd)

    def test_uls_level_with_creep_softens_the_curvature_curve(self) -> None:
        """An explicit effective modulus softens the elastic branch of the ULS moment-curvature curve."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        section = build_concrete_section(_section(), level=AnalysisLevel.ULS, elastic_modulus=concrete.e_cm / 2)
        profile = section.concrete_geometries[0].material.stress_strain_profile
        strain = 0.5 * concrete.f_cd / concrete.e_cm
        assert profile.get_stress(strain) == pytest.approx(0.5 * concrete.f_cd / 2)

    def test_uls_level_maps_design_steel(self) -> None:
        """The ULS reinforcement yields at the design strength f_yd."""
        section = build_concrete_section(_section(), level=AnalysisLevel.ULS)
        bar_profile = section.reinf_geometries_lumped[0].material.stress_strain_profile
        assert bar_profile.yield_strength == pytest.approx(ReinforcementSteelMaterial().f_yd)

    def test_distinct_materials_map_to_distinct_bars(self) -> None:
        """Two different reinforcement materials produce two distinct backend SteelBar instances."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=-200, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=200, material=ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500C)))
        section = build_concrete_section(cs)
        bar_materials = {id(geom.material) for geom in section.reinf_geometries_lumped}
        assert len(bar_materials) == 2

    def test_same_material_reuses_one_bar(self) -> None:
        """Rebars of the same material reuse a single backend SteelBar instance."""
        section = build_concrete_section(_section())
        bar_materials = {id(geom.material) for geom in section.reinf_geometries_lumped}
        assert len(bar_materials) == 1

    def test_coincident_corner_bars_are_merged(self) -> None:
        """Bars shared between adjacent edges (12 bars, 4 coincident corners) merge to 8 distinct bars."""
        cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        for edge in ("lower", "upper", "left", "right"):
            cs.add_longitudinal_reinforcement_by_quantity(n=3, diameter=20, edge=edge, material=ReinforcementSteelMaterial())
        assert len(cs.longitudinal_rebars) == 12
        section = build_concrete_section(cs)
        assert len(section.reinf_geometries_lumped) == 8

    def test_merged_corner_bar_has_combined_area(self) -> None:
        """Two coincident 20 mm bars merge into one bar with the summed area (about sqrt(2) x diameter)."""
        cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=150, y=150, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=150, y=150, material=ReinforcementSteelMaterial()))
        single_area = 3.141592653589793 / 4 * 20**2
        section = build_concrete_section(cs)
        assert len(section.reinf_geometries_lumped) == 1
        # the backend polygonizes the circle, so the meshed area is within ~0.5% of the requested area
        assert section.reinf_geometries_lumped[0].calculate_area() == pytest.approx(2 * single_area, rel=1e-2)

    def test_coincident_bars_with_different_materials_raise(self) -> None:
        """Coincident bars of different materials cannot be merged and raise a clear error."""
        cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=0, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=0, material=ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500C)))
        with pytest.raises(ValueError, match="different materials"):
            build_concrete_section(cs)


class TestEffectiveModulus:
    """Tests for the effective-modulus helper E_c,eff = E_cm / (1 + phi)."""

    def test_zero_creep_returns_e_cm(self) -> None:
        """With phi = 0 (short-term) the effective modulus is the secant modulus e_cm."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        assert effective_modulus(concrete, 0.0) == concrete.e_cm

    def test_creep_divides_by_one_plus_phi(self) -> None:
        """With phi = 1 the effective modulus halves."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        assert effective_modulus(concrete, 1.0) == pytest.approx(concrete.e_cm / 2.0)

    def test_negative_creep_raises(self) -> None:
        """A negative creep coefficient is rejected."""
        with pytest.raises(ValueError, match="creep coefficient"):
            effective_modulus(ConcreteMaterial(ConcreteStrengthClass.C30_37), -0.1)


class TestUltimateProfile:
    """Tests for the ultimate stress-strain profile mapping."""

    def test_bilinear_diagram(self) -> None:
        """A BILINEAR concrete diagram maps to a BilinearStressStrain ultimate profile with converted strains."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37, diagram_type=DiagramType.BILINEAR)
        profile = _ultimate_profile(concrete)
        assert type(profile).__name__ == "BilinearStressStrain"
        assert profile.compressive_strain == pytest.approx(concrete.eps_c3 * PER_MILLE_TO_RATIO)

    def test_parabolic_diagram(self) -> None:
        """A PARABOLIC concrete diagram maps to a EurocodeParabolicUltimate ultimate profile."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37, diagram_type=DiagramType.PARABOLIC)
        profile = _ultimate_profile(concrete)
        assert type(profile).__name__ == "EurocodeParabolicUltimate"

    def test_user_diagram_not_implemented(self) -> None:
        """A USER concrete diagram is not supported by the backend mapping."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37, diagram_type=DiagramType.USER)
        with pytest.raises(NotImplementedError, match="User defined"):
            _ultimate_profile(concrete)


class TestSteelMapping:
    """Tests for the reinforcement steel mapping."""

    def test_elastic_plastic_profile_from_characteristic_values(self) -> None:
        """SLS steel is elastic-plastic at f_yk/E_s with the fracture strain converted from per mille."""
        material = ReinforcementSteelMaterial()
        bar = _service_steel(material)
        profile = bar.stress_strain_profile
        assert profile.yield_strength == material.f_yk
        assert profile.elastic_modulus == material.e_s
        assert profile.fracture_strain == pytest.approx(material.eps_uk * PER_MILLE_TO_RATIO)

    def test_ultimate_horizontal_branch_is_elastic_plastic_at_f_yd(self) -> None:
        """The default ULS diagram is elastic-plastic at f_yd/E_s (horizontal branch, art. 3.2.7(2)(b))."""
        material = ReinforcementSteelMaterial()
        profile = _ultimate_steel(material).stress_strain_profile
        assert type(profile).__name__ == "SteelElasticPlastic"
        assert profile.yield_strength == pytest.approx(material.f_yd)
        assert profile.elastic_modulus == material.e_s
        assert profile.fracture_strain == pytest.approx(material.eps_uk * PER_MILLE_TO_RATIO)

    def test_ultimate_inclined_branch_hardens_to_eps_ud(self) -> None:
        """The inclined ULS diagram rises towards k*f_yd at eps_uk and is cut off at eps_ud = 0.9*eps_uk."""
        material = ReinforcementSteelMaterial()  # B500B: k = 1.08, eps_uk = 50 per mille
        profile = _ultimate_steel(material, branch=SteelBranch.INCLINED).stress_strain_profile
        eps_uk = material.eps_uk / 1000
        eps_yd = material.f_yd / material.e_s
        eps_ud = 0.9 * eps_uk
        expected_stress = material.f_yd * (1 + (material.ductility_factor_k - 1) * (eps_ud - eps_yd) / (eps_uk - eps_yd))
        assert type(profile).__name__ == "SteelHardening"
        assert profile.fracture_strain == pytest.approx(eps_ud)
        assert profile.ultimate_strength == pytest.approx(expected_stress)
        # the inclined design branch stays below the characteristic tensile strength k*f_yk
        assert profile.ultimate_strength < material.ductility_factor_k * material.f_yk


class TestDeduplicatePslg:
    """The meshing guard removes duplicate vertices before the graph reaches Triangle.

    A repeated vertex makes the meshing backend read past the end of its output buffer, which crashes the
    interpreter on some heap layouts and silently corrupts the meshed capacity on others.
    """

    def test_removes_duplicate_vertex_and_remaps_segments(self) -> None:
        """A repeated vertex is dropped and the segments are renumbered onto the surviving vertices."""
        tri = {
            "vertices": [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (100.0, 100.0)],
            "segments": [(0, 1), (1, 2), (2, 3), (3, 0)],
        }
        guarded = _deduplicate_pslg(tri)
        assert guarded["vertices"] == [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0)]
        # the (2, 3) segment collapsed onto a single vertex and is gone; the closing segment now ends at 2
        assert guarded["segments"] == [(0, 1), (1, 2), (2, 0)]

    def test_keeps_other_keys(self) -> None:
        """Keys the backend sets besides vertices and segments (such as holes) are carried over untouched."""
        holes = [(50.0, 50.0)]
        tri = {
            "vertices": [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (100.0, 100.0)],
            "segments": [(0, 1), (1, 2), (2, 3), (3, 0)],
            "holes": holes,
        }
        assert _deduplicate_pslg(tri)["holes"] == holes

    def test_graph_without_duplicates_is_returned_unchanged(self) -> None:
        """A clean graph is handed on as-is, so the guard costs nothing for the vast majority of calls."""
        tri = {"vertices": [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0)], "segments": [(0, 1), (1, 2), (2, 0)]}
        assert _deduplicate_pslg(tri) is tri

    def test_degenerate_sliver_is_left_alone(self) -> None:
        """A graph that would shrink below three vertices is passed through: the backend handles those itself.

        Deduplicating a zero-area sliver would leave fewer vertices than the backend accepts, so it would turn
        a harmless "no triangles" result into an error.
        """
        tri = {"vertices": [(0.0, 0.0), (0.0, 100.0), (0.0, 100.0)], "segments": [(0, 1), (1, 2), (2, 0)]}
        assert _deduplicate_pslg(tri) is tri


class TestGuardDegenerateMeshes:
    """The guard is swapped into the backend's namespace for the duration of an analysis and taken out after."""

    def test_installs_and_restores_the_meshing_module(self) -> None:
        """Inside the context the backend meshes through the guard; afterwards its own module is back."""
        original = backend_analysis_section.triangle
        with _guard_degenerate_meshes():
            assert getattr(backend_analysis_section.triangle, _MESH_GUARD_FLAG, False)
            assert backend_analysis_section.triangle is not original
        assert backend_analysis_section.triangle is original

    def test_nesting_does_not_stack_guards(self) -> None:
        """Nested backend calls reuse the guard already in place instead of wrapping it twice."""
        with _guard_degenerate_meshes():
            installed = backend_analysis_section.triangle
            with _guard_degenerate_meshes():
                assert backend_analysis_section.triangle is installed
            assert backend_analysis_section.triangle is installed

    def test_restores_the_module_when_the_analysis_raises(self) -> None:
        """A failing analysis must not leave the guard behind in the backend's namespace."""
        original = backend_analysis_section.triangle
        with pytest.raises(ValueError, match="boom"), _guard_degenerate_meshes():
            raise ValueError("boom")
        assert backend_analysis_section.triangle is original

    def test_serves_other_attributes_from_the_wrapped_module(self) -> None:
        """Only triangulate is intercepted; anything else the backend reads comes from the real module."""
        original = backend_analysis_section.triangle
        with _guard_degenerate_meshes():
            guard = backend_analysis_section.triangle
            assert guard.__name__ == original.__name__
            assert guard.triangulate is not original.triangulate
            assert {name for name in vars(original) if not name.startswith("_")} <= set(vars(guard))

    def test_triangulates_a_graph_with_a_duplicate_vertex(self) -> None:
        """The guarded call meshes the deduplicated graph and returns a usable mesh."""
        tri = {
            "vertices": [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (100.0, 100.0)],
            "segments": [(0, 1), (1, 2), (2, 3), (3, 0)],
        }
        with _guard_degenerate_meshes():
            mesh = backend_analysis_section.triangle.triangulate(tri, "p")
        assert len(mesh["vertices"]) == 3
        assert len(mesh["triangles"]) == 1
