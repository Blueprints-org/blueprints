"""Tests for the concreteproperties adapter (material mapping and section building)."""

import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass, DiagramType
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    AnalysisLevel,
    _service_steel,
    _ultimate_profile,
    build_concrete_section,
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
        """The concrete service profile carries the secant modulus e_cm."""
        section = build_concrete_section(_section())
        concrete_material = section.concrete_geometries[0].material
        assert concrete_material.stress_strain_profile.elastic_modulus == ConcreteMaterial(ConcreteStrengthClass.C30_37).e_cm

    def test_flexural_tensile_strength_from_formula_3_23(self) -> None:
        """flexural_tensile_strength = f_ctm,fl for the 500 mm member height: (1.6 - 500/1000) * f_ctm."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        section = build_concrete_section(_section())
        assert section.concrete_geometries[0].material.flexural_tensile_strength == pytest.approx((1.6 - 500 / 1000) * concrete.f_ctm)

    def test_adds_one_lumped_bar_per_rebar(self) -> None:
        """Each longitudinal rebar becomes one lumped reinforcement bar."""
        section = build_concrete_section(_section())
        assert len(section.reinf_geometries_lumped) == 4

    def test_uls_level_not_implemented(self) -> None:
        """Only the SLS level is implemented; ULS raises."""
        with pytest.raises(NotImplementedError, match="ULS"):
            build_concrete_section(_section(), level=AnalysisLevel.ULS)

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
