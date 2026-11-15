"""Sign- and unit-convention tests for the analysis adapter, using the real backend.

These pin the single conversion point in ``_adapter.py``: Blueprints is tension-positive / compression-
negative in kN/kNm; the backend is the opposite. An asymmetric section and a pure-axial case are
mandatory (issue #1061). Not marked slow on purpose — this is the coverage that proves the adapter.
"""

import warnings

import numpy as np
import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _bare_section() -> RectangularReinforcedCrossSection:
    return RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))


def _symmetric_analysis() -> CrossSectionAnalysis:
    """Top-bottom symmetric reinforcement: the transformed centroid coincides with the outline centroid."""
    cs = _bare_section()
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="upper")
    return CrossSectionAnalysis(cs)


class TestNormalForceSign:
    """Pin the normal-force sign (Blueprints tension positive, compression negative)."""

    def test_compression_is_negative(self) -> None:
        """A compressive (negative) normal force yields compressive (negative) concrete stresses."""
        result = _symmetric_analysis().stress(SectionForces(n=-1000), regime=Regime.SLS_UNCRACKED)
        assert result.concrete_stress_min < 0
        assert result.concrete_stress_max < 0

    def test_tension_is_positive(self) -> None:
        """A tensile (positive) normal force yields tensile (positive) concrete stresses."""
        result = _symmetric_analysis().stress(SectionForces(n=500), regime=Regime.SLS_UNCRACKED)
        assert result.concrete_stress_max > 0

    def test_pure_axial_is_uniform_and_does_not_warn(self) -> None:
        """Pure axial force gives a uniform stress field and the backend divide warning is suppressed."""
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            result = _symmetric_analysis().stress(SectionForces(n=-1000), regime=Regime.SLS_UNCRACKED)
        assert result.concrete_stress_min == pytest.approx(result.concrete_stress_max, rel=1e-9)


class TestMomentSign:
    """Pin the bending-moment axis mapping and sign on an asymmetric layout."""

    def test_positive_m_y_tensions_the_bottom(self) -> None:
        """Positive m_y (about the y-axis) tensions the bottom fibre and compresses the top."""
        cs = _bare_section()
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=-100, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=100, material=ReinforcementSteelMaterial()))
        result = CrossSectionAnalysis(cs).stress(SectionForces(m_y=100), regime=Regime.SLS_UNCRACKED)
        bottom = next(r for r in result.rebar_results if r.y < 0)
        top = next(r for r in result.rebar_results if r.y > 0)
        assert bottom.stress > 0
        assert top.stress < 0

    @pytest.mark.parametrize("regime", [Regime.SLS_UNCRACKED, Regime.SLS_CRACKED])
    def test_positive_m_z_tensions_the_negative_y_side(self, regime: Regime) -> None:
        """Positive m_z (rotation from x to y, SAF) tensions the -y side (section -x) and compresses the +y side, in both regimes."""
        cs = _bare_section()
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=-100, y=0, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=100, y=0, material=ReinforcementSteelMaterial()))
        result = CrossSectionAnalysis(cs).stress(SectionForces(m_z=100), regime=regime)
        positive = next(r for r in result.rebar_results if r.x > 0)
        negative = next(r for r in result.rebar_results if r.x < 0)
        assert negative.stress > 0
        assert negative.stress > positive.stress
        assert result.strain_plane.strain_at(-150, 0) > 0
        assert result.strain_plane.strain_at(150, 0) < 0


class TestAxialMagnitude:
    """Pin the unit conversion against a transformed-section hand calculation."""

    def test_uniform_axial_stress_matches_transformed_section(self) -> None:
        """Pure axial stress on a symmetric section equals N / A_transformed (compression negative)."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        bar_area = 3.141592653589793 / 4 * 20**2
        a_transformed = 300 * 500 + (steel.e_s / concrete.e_cm - 1) * 8 * bar_area
        expected = -1000e3 / a_transformed  # N / mm^2, compression negative
        result = _symmetric_analysis().stress(SectionForces(n=-1000), regime=Regime.SLS_UNCRACKED)
        assert result.concrete_stress_min == pytest.approx(expected, rel=1e-2)
        assert result.concrete_stress_max == pytest.approx(expected, rel=1e-2)

    def test_axial_force_acts_at_the_outline_centroid(self) -> None:
        """With bottom bars only, N at mid-height sits above the transformed centroid and adds N * e of bending.

        Hand calculation on the transformed section: sigma = N / A_tr + N * e * (y - y_tr) / I_tr, with e the
        distance from the transformed centroid up to the outline centroid.
        """
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        cs = _bare_section()
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=steel, edge="lower")
        bar_y = cs.longitudinal_rebars[0].y
        added = (steel.e_s / concrete.e_cm - 1) * 4 * 3.141592653589793 / 4 * 20**2  # bars, net of the displaced concrete
        a_transformed = 300 * 500 + added
        y_transformed = added * bar_y / a_transformed  # below mid-height
        i_transformed = 300 * 500**3 / 12 + 300 * 500 * y_transformed**2 + added * (bar_y - y_transformed) ** 2
        n = -1000e3
        e = 0.0 - y_transformed

        def stress(y: float) -> float:
            return n / a_transformed + n * e * (y - y_transformed) / i_transformed

        result = CrossSectionAnalysis(cs).stress(SectionForces(n=-1000), regime=Regime.SLS_UNCRACKED)
        assert result.concrete_stress_min == pytest.approx(stress(250.0), rel=1e-2)  # top fibre, most compressed
        assert result.concrete_stress_max == pytest.approx(stress(-250.0), rel=1e-2)


class TestUnsymmetricBiaxialReference:
    """Pin both bending components on a section without any symmetry against an independent strain-plane solution."""

    def test_uncracked_strain_plane_matches_the_transformed_section_equilibrium(self) -> None:
        """Solve the strain plane eps = eps_0 + a x + b y of the transformed section by hand and compare.

        Equilibrium about the outline centroid, in Blueprints conventions (tension positive):
        n = integral of sigma, m_z = -integral of sigma * x (tension on the -x side), m_y = -integral of sigma * y
        (tension at the bottom). The bars are lumped at their centres with (alpha_e - 1) * A_s.
        """
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        width, height = 300.0, 500.0
        bars = [(-100.0, -200.0, 25.0), (80.0, -210.0, 20.0), (60.0, 200.0, 16.0)]
        cs = _bare_section()
        for x, y, diameter in bars:
            cs.add_longitudinal_rebar(Rebar(diameter=diameter, x=x, y=y, material=steel))
        forces = SectionForces(n=-200, m_y=40, m_z=15)

        added = [(steel.e_s / concrete.e_cm - 1) * np.pi / 4 * d**2 for _, _, d in bars]
        area = width * height + sum(added)
        q_x = sum(a * x for a, (x, _, _) in zip(added, bars, strict=True))
        q_y = sum(a * y for a, (_, y, _) in zip(added, bars, strict=True))
        i_xx = height * width**3 / 12 + sum(a * x**2 for a, (x, _, _) in zip(added, bars, strict=True))
        i_xy = sum(a * x * y for a, (x, y, _) in zip(added, bars, strict=True))
        i_yy = width * height**3 / 12 + sum(a * y**2 for a, (_, y, _) in zip(added, bars, strict=True))
        stiffness = concrete.e_cm * np.array([[area, q_x, q_y], [q_x, i_xx, i_xy], [q_y, i_xy, i_yy]])
        actions = np.array([forces.n * 1e3, -forces.m_z * 1e6, -forces.m_y * 1e6])  # N, Nmm
        eps_0, a, b = np.linalg.solve(stiffness, actions)

        def strain(x: float, y: float) -> float:
            return (eps_0 + a * x + b * y) * 1e3  # per mille

        result = CrossSectionAnalysis(cs).stress(forces, regime=Regime.SLS_UNCRACKED)
        for rebar in result.rebar_results:
            assert rebar.strain == pytest.approx(strain(rebar.x, rebar.y), rel=1e-2)
        corners = [concrete.e_cm * strain(x, y) / 1e3 for x in (-150, 150) for y in (-250, 250)]
        assert result.concrete_stress_min == pytest.approx(min(corners), rel=1e-2)
        assert result.concrete_stress_max == pytest.approx(max(corners), rel=1e-2)
