"""Tests for the moment-curvature analysis (behaviour, creep, plot and error paths).

Numerical anchors (cracking moment, uncracked stiffness, ultimate moment vs M_Rd) live in
``test_benchmarks.py``; these tests pin the API behaviour.
"""

import math

import matplotlib as mpl
import numpy as np
import pytest

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from concreteproperties.utils import AnalysisError

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, MomentCurvatureResult, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import AnalysisLevel
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.cross_section_analysis import _dominant_moment_direction
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _analysis() -> CrossSectionAnalysis:
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


def _secant_stiffness(result: MomentCurvatureResult, kappa: float) -> float:
    """Secant stiffness M / kappa at the given curvature, interpolated on the traced curve [kNm*mm]."""
    return float(np.interp(kappa, result.kappa, result.m)) / kappa


class TestMomentCurvature:
    """Structure of the traced moment-curvature curve."""

    @pytest.mark.slow
    def test_curve_is_traced_to_failure(self) -> None:
        """The curve holds matching arrays with increasing curvature and a positive peak moment."""
        result = _analysis().moment_curvature()
        assert isinstance(result, MomentCurvatureResult)
        assert len(result.kappa) == len(result.m) == len(result.m_y) == len(result.m_z)
        assert all(k2 > k1 for k1, k2 in zip(result.kappa[:-1], result.kappa[1:], strict=True))
        assert result.m_ultimate > 0
        # uniaxial sagging: the resultant moment is the y-component
        assert result.m[-1] == pytest.approx(abs(result.m_y[-1]))

    @pytest.mark.slow
    def test_creep_softens_the_elastic_branch(self) -> None:
        """A positive creep coefficient lowers the secant stiffness of the early (elastic) branch."""
        analysis = _analysis()
        short_term = analysis.moment_curvature()
        long_term = analysis.moment_curvature(creep_coefficient=2.0)
        kappa_probe = 5e-7  # well inside the uncracked branch
        assert _secant_stiffness(long_term, kappa_probe) < 0.5 * _secant_stiffness(short_term, kappa_probe)

    @pytest.mark.slow
    def test_plot_returns_figure(self) -> None:
        """plot() returns a matplotlib figure with the moment-curvature axes."""
        figure = _analysis().moment_curvature().plot()
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            assert "1/mm" in ax.get_xlabel()
            assert "kNm" in ax.get_ylabel()
        finally:
            plt.close(figure)


class TestTensionStiffening:
    """The EN 1992-1-1 art. 7.4.3 mean-curvature interpolation (tension_stiffening=True)."""

    @pytest.mark.slow
    def test_flag_moments_preserved_and_curve_is_stiffer(self) -> None:
        """The mean curve keeps the moments and ultimate, flags itself, and is stiffer once cracked."""
        analysis = _analysis()
        bare = analysis.moment_curvature()
        mean = analysis.moment_curvature(tension_stiffening=True)
        assert bare.tension_stiffening is False
        assert mean.tension_stiffening is True
        assert mean.m == bare.m  # only the curvatures change
        assert mean.m_ultimate == bare.m_ultimate
        # tension stiffening can only stiffen: every mean curvature is <= the bare one.
        assert all(km <= kb + 1e-12 for km, kb in zip(mean.kappa, bare.kappa, strict=True))
        # and strictly stiffer somewhere in the cracked range.
        assert any(km < kb - 1e-9 for km, kb in zip(mean.kappa, bare.kappa, strict=True))

    @pytest.mark.slow
    def test_uncracked_branch_is_unchanged(self) -> None:
        """Below the cracking moment the section is uncracked, so the mean curvature equals the bare one."""
        analysis = _analysis()
        bare = analysis.moment_curvature()
        mean = analysis.moment_curvature(tension_stiffening=True)
        m_cr = analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_CRACKED).cracked_properties.m_cr
        for km, kb, moment in zip(mean.kappa, bare.kappa, bare.m, strict=True):
            if moment < m_cr:
                assert km == kb

    @pytest.mark.slow
    def test_matches_en_7_18_7_19_interpolation(self) -> None:
        """At a cracked point the mean curvature equals the closed-form zeta interpolation of art. 7.4.3."""
        analysis = _analysis()
        bare = analysis.moment_curvature()
        mean = analysis.moment_curvature(tension_stiffening=True)
        m_cr = analysis.stress(SectionForces(m_y=100), regime=Regime.SLS_CRACKED).cracked_properties.m_cr
        # a traced point well above cracking
        index = min(range(len(bare.m)), key=lambda i: abs(bare.m[i] - 2.0 * m_cr))
        moment = bare.m[index]
        uncracked = analysis.stress(SectionForces(m_y=moment), regime=Regime.SLS_UNCRACKED)
        kappa_uncracked = math.hypot(uncracked.strain_plane.kappa_y, uncracked.strain_plane.kappa_z)
        zeta = 1.0 - 1.0 * (m_cr / moment) ** 2
        expected = zeta * bare.kappa[index] + (1.0 - zeta) * kappa_uncracked
        assert mean.kappa[index] == pytest.approx(expected, rel=1e-3)

    @pytest.mark.slow
    def test_sustained_load_still_stiffens(self) -> None:
        """With creep (sustained load, beta = 0.5) the mean curve is still flagged and stiffer than bare."""
        analysis = _analysis()
        bare = analysis.moment_curvature(creep_coefficient=2.0)
        mean = analysis.moment_curvature(creep_coefficient=2.0, tension_stiffening=True)
        assert mean.tension_stiffening is True
        assert any(km < kb - 1e-9 for km, kb in zip(mean.kappa, bare.kappa, strict=True))

    @pytest.mark.parametrize(
        ("m_y", "m_z", "expected"),
        [
            (100.0, 0.01, (1.0, 0.0)),  # y-dominant: the tiny z-component is snapped to zero
            (0.01, 100.0, (0.0, 1.0)),  # z-dominant: the tiny y-component is snapped to zero
        ],
    )
    def test_dominant_moment_direction_snaps_a_negligible_component(self, m_y: float, m_z: float, expected: tuple[float, float]) -> None:
        """The direction helper keeps a nominally uniaxial trace uniaxial by zeroing the negligible axis."""
        result = MomentCurvatureResult(theta=0.0, n=0.0, kappa=(1e-6,), m_y=(m_y,), m_z=(m_z,), m=(math.hypot(m_y, m_z),), raw=None)
        assert _dominant_moment_direction(result) == pytest.approx(expected)

    @pytest.mark.slow
    def test_biaxial_trace_is_rejected(self) -> None:
        """Tension stiffening on a biaxial trace routes through the cracked analysis, which is uniaxial."""
        with pytest.raises(NotImplementedError, match="biaxial bending"):
            _analysis().moment_curvature(theta=45.0, tension_stiffening=True)


class TestErrorPaths:
    """Clear errors for unsupported inputs and solver failures."""

    def test_without_rebars_raises(self) -> None:
        """A moment-curvature analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Moment-curvature analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).moment_curvature()

    def test_negative_creep_coefficient_raises(self) -> None:
        """A negative creep coefficient is rejected."""
        with pytest.raises(ValueError, match="creep coefficient"):
            _analysis().moment_curvature(creep_coefficient=-1.0)

    def test_non_convergence_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend AnalysisError is re-raised as a clear ValueError with context."""
        analysis = _analysis()
        section = analysis._backend_section(AnalysisLevel.ULS)  # noqa: SLF001 — exercising the cached backend section

        def failing_curvature(*_args: object, **_kwargs: object) -> object:
            raise AnalysisError("equilibrium not found")

        monkeypatch.setattr(section, "moment_curvature_analysis", failing_curvature)
        with pytest.raises(ValueError, match="did not converge"):
            analysis.moment_curvature()
