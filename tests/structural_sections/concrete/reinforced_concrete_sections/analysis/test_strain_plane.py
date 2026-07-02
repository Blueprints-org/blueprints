"""Strain-plane reconstruction tests, using the real backend. Not marked slow on purpose.

These pin the plane the analyzer fits from the backend's stresses/strains: the reconstructed strain at
each rebar must match that rebar's own strain, the neutral axis must line up with the cracked-section
result, and the pure-axial / all-tension degeneracies must fall back cleanly. The under-determined and
consistency-check guards are exercised directly with crafted inputs.
"""

import numpy as np
import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    _reconstruct_strain_plane,
    _validate_reconstruction,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _analysis() -> CrossSectionAnalysis:
    """Reference 300 x 500 C30/37 section with 4 D20 B500B on the lower edge."""
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


class TestReconstructionAgainstRebars:
    """The fitted plane must reproduce each rebar's strain independently of the backend internals."""

    def test_uncracked_plane_matches_rebar_strains(self) -> None:
        """strain_at(rebar) equals the rebar's own strain for an uncracked N + M_y state."""
        result = _analysis().uncracked_stress(SectionForces(n=-300, m_y=40))
        plane = result.strain_plane
        assert plane is not None
        for rebar in result.rebar_results:
            assert plane.strain_at(rebar.x, rebar.y) == pytest.approx(rebar.strain, rel=1e-6, abs=1e-9)

    def test_cracked_plane_matches_rebar_strains(self) -> None:
        """strain_at(rebar) equals the rebar's own strain for a cracked M_y state."""
        result = _analysis().cracked_stress(SectionForces(m_y=150))
        plane = result.strain_plane
        assert plane is not None
        for rebar in result.rebar_results:
            assert plane.strain_at(rebar.x, rebar.y) == pytest.approx(rebar.strain, rel=1e-6, abs=1e-9)


class TestNeutralAxis:
    """Neutral-axis geometry derived from the plane."""

    def test_uniaxial_bending_gives_horizontal_neutral_axis(self) -> None:
        """Pure m_y bending yields a horizontal neutral axis (angle ~ 0 deg)."""
        plane = _analysis().uncracked_stress(SectionForces(m_y=100)).strain_plane
        assert plane is not None
        assert plane.neutral_axis_angle == pytest.approx(0.0, abs=1e-6)

    def test_cracked_neutral_axis_depth_matches_cracked_properties(self) -> None:
        """The plane's neutral-axis depth agrees with the cracked-section result."""
        analysis = _analysis()
        forces = SectionForces(m_y=150)
        plane = analysis.cracked_stress(forces).strain_plane
        assert plane is not None
        expected = analysis.cracked_properties(forces).neutral_axis_depth
        assert plane.neutral_axis_depth == pytest.approx(expected, rel=0.02)

    def test_pure_axial_has_no_neutral_axis(self) -> None:
        """A pure axial force gives a flat strain plane: no curvature, no neutral axis."""
        plane = _analysis().uncracked_stress(SectionForces(n=-1000)).strain_plane
        assert plane is not None
        assert plane.neutral_axis_depth is None
        assert plane.neutral_axis_angle == 0.0
        assert plane.strain_at(0, 250) == pytest.approx(plane.strain_at(0, -250))

    def test_all_tension_section_has_no_neutral_axis(self) -> None:
        """A large tensile force with slight bending keeps every fibre in tension: no neutral axis."""
        plane = _analysis().uncracked_stress(SectionForces(n=3000, m_y=5)).strain_plane
        assert plane is not None
        assert plane.neutral_axis_depth is None


class _FakeGeometry:
    def __init__(self, centroid: tuple[float, float]) -> None:
        self._centroid = centroid

    def calculate_centroid(self) -> tuple[float, float]:
        return self._centroid


class _FakeSection:
    def __init__(self, nodes: list[list[float]]) -> None:
        self.mesh_nodes = np.array(nodes, dtype=float)


class _FakeRaw:
    """Minimal stand-in for a backend StressResult for the guard branches."""

    def __init__(self, nodes: list[list[float]], stresses: list[float], rebar_xy: tuple[float, float], rebar_strain: float) -> None:
        self.concrete_analysis_sections = [_FakeSection(nodes)]
        self.concrete_stresses = [np.array(stresses, dtype=float)]
        self.lumped_reinforcement_geometries = [_FakeGeometry(rebar_xy)]
        self.lumped_reinforcement_strains = [rebar_strain]


class TestGuards:
    """The under-determined and consistency-check guards."""

    def test_underdetermined_plane_raises(self) -> None:
        """Collinear strain samples (single rebar layer, no spread in y) cannot define the plane."""
        raw = _FakeRaw(nodes=[[0, 100], [100, 100], [200, 100]], stresses=[1.0, 1.0, 1.0], rebar_xy=(50, 100), rebar_strain=-5e-4)
        with pytest.raises(ValueError, match="under-determined"):
            _reconstruct_strain_plane(raw, elastic_modulus=33000, is_cracked=True, concrete_stress_min=-1.0, concrete_stress_max=0.0)

    def test_reconstruction_mismatch_raises(self) -> None:
        """A fitted plane whose stresses disagree with the backend envelope raises a clear error."""
        node_coords = np.array([[0.0, 250.0], [0.0, -250.0]])
        with pytest.raises(RuntimeError, match="consistency check"):
            _validate_reconstruction(
                node_coords,
                eps_0=0.0,
                kappa_z=0.0,
                kappa_y=0.0,
                elastic_modulus=33000,
                is_cracked=False,
                concrete_stress_min=-10.0,  # deliberately inconsistent with the flat (zero-stress) plane
                concrete_stress_max=10.0,
            )
