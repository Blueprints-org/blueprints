"""Cross-check of the ULS capacity against ``structuralcodes`` (an independent EC2 engine).

``structuralcodes`` implements EN 1992 with its own fibre integrator, so agreement is strong external
validation on top of the closed-form anchors in ``test_benchmarks.py``. It is an optional test-only
oracle: the module is skipped when the package is not installed (it is not a project dependency).

The comparison uses the parabola-rectangle concrete diagram and the inclined steel branch on the
Blueprints side, matching the ``structuralcodes`` defaults (parabola-rectangle concrete, hardening
reinforcement from ftk/epsuk).
"""

import pytest

pytest.importorskip("concreteproperties")
pytest.importorskip("structuralcodes")

from shapely import Polygon
from structuralcodes import set_design_code
from structuralcodes.geometry import SurfaceGeometry, add_reinforcement
from structuralcodes.materials.concrete import create_concrete
from structuralcodes.materials.reinforcement import create_reinforcement
from structuralcodes.sections import BeamSection

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass, DiagramType
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, SteelBranch
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection

WIDTH = 300.0
HEIGHT = 500.0


def _blueprints_analysis() -> CrossSectionAnalysis:
    """300 x 500 C30/37 (parabola-rectangle), 4 D20 B500B lower edge, inclined steel branch."""
    concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37, diagram_type=DiagramType.PARABOLIC)
    cs = RectangularReinforcedCrossSection(width=WIDTH, height=HEIGHT, concrete_material=concrete)
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs, steel_branch=SteelBranch.INCLINED)


def _structuralcodes_section() -> BeamSection:
    """The same section in structuralcodes (fck=30, B500B: fyk=500, ftk=540, epsuk=5%)."""
    set_design_code("ec2_2004")
    concrete = create_concrete(fck=30)
    reinforcement = create_reinforcement(fyk=500, Es=200000, density=7850, ftk=540, epsuk=0.05)
    geometry = SurfaceGeometry(
        Polygon([(-WIDTH / 2, -HEIGHT / 2), (WIDTH / 2, -HEIGHT / 2), (WIDTH / 2, HEIGHT / 2), (-WIDTH / 2, HEIGHT / 2)]),
        concrete,
    )
    blueprints_section = _blueprints_analysis()._cross_section  # noqa: SLF001 — reuse the exact bar layout
    for rebar in blueprints_section.longitudinal_rebars:
        geometry = add_reinforcement(geometry, (rebar.x, rebar.y), rebar.diameter, reinforcement)
    return BeamSection(geometry)


@pytest.mark.slow
class TestStructuralcodesOracle:
    """Blueprints ULS capacities against the independent structuralcodes engine."""

    def test_pure_bending_capacity_matches(self) -> None:
        """Pure-bending M_Rd agrees with structuralcodes within 0.5%."""
        blueprints_m_rd = _blueprints_analysis().bending_capacity().m_rd
        oracle = _structuralcodes_section().section_calculator.calculate_bending_strength(theta=0, n=0)
        assert blueprints_m_rd == pytest.approx(abs(oracle.m_y) / 1e6, rel=0.005)

    def test_bending_capacity_with_compression_matches(self) -> None:
        """M_Rd at N = -500 kN (an N-M interaction point) agrees with structuralcodes within 0.5%."""
        blueprints_m_rd = _blueprints_analysis().bending_capacity(n=-500.0).m_rd
        oracle = _structuralcodes_section().section_calculator.calculate_bending_strength(theta=0, n=-500e3)
        assert blueprints_m_rd == pytest.approx(abs(oracle.m_y) / 1e6, rel=0.005)
