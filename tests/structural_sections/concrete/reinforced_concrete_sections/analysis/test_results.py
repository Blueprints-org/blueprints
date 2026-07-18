"""Tests for the analysis result dataclasses.

Importing the analysis package pulls in the ``_adapter`` module, which requires the optional
``concreteproperties`` backend, so the whole module is skipped when that backend is absent.
"""

import pytest

pytest.importorskip("concreteproperties")

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import (
    CrackedProperties,
    RebarStressResult,
    Regime,
    StrainPlane,
    StressStrainResult,
)
from blueprints.structural_sections.section_forces import SectionForces


class TestRebarStressResult:
    """Tests for RebarStressResult."""

    def test_stores_fields(self) -> None:
        """All fields are stored as given."""
        rebar = RebarStressResult(x=10.0, y=-20.0, diameter=20.0, stress=-30.0, strain=-0.15, force=-9.4)
        assert (rebar.x, rebar.y, rebar.diameter, rebar.stress, rebar.strain, rebar.force) == (10.0, -20.0, 20.0, -30.0, -0.15, -9.4)

    def test_is_frozen(self) -> None:
        """RebarStressResult is immutable."""
        rebar = RebarStressResult(x=0.0, y=0.0, diameter=20.0, stress=0.0, strain=0.0, force=0.0)
        with pytest.raises(AttributeError):
            rebar.stress = 1.0  # type: ignore[misc]


class _FakeRaw:
    """Minimal stand-in for a backend StressResult, recording plot_stress calls."""

    def __init__(self) -> None:
        self.calls: list[tuple[tuple, dict]] = []

    def plot_stress(self, *args: object, **kwargs: object) -> str:
        self.calls.append((args, kwargs))
        return "plotted"


class TestStressStrainResult:
    """Tests for StressStrainResult."""

    def _result(self, raw: object) -> StressStrainResult:
        return StressStrainResult(
            forces=SectionForces(n=-100.0, m_y=150.0),
            regime=Regime.SLS_UNCRACKED,
            concrete_stress_min=-7.5,
            concrete_stress_max=2.0,
            rebar_results=[RebarStressResult(x=0.0, y=-200.0, diameter=20.0, stress=35.0, strain=0.18, force=11.0)],
            raw=raw,
        )

    def test_stores_fields(self) -> None:
        """The result echoes the forces and carries the stress envelope and rebar results."""
        result = self._result(raw=_FakeRaw())
        assert result.forces == SectionForces(n=-100.0, m_y=150.0)
        assert result.regime is Regime.SLS_UNCRACKED
        assert result.concrete_stress_min == -7.5
        assert result.concrete_stress_max == 2.0
        assert len(result.rebar_results) == 1

    @pytest.mark.parametrize(
        ("regime", "expected"),
        [
            (Regime.SLS_UNCRACKED, False),
            (Regime.SLS_CRACKED, True),
            (Regime.ULS, False),
        ],
    )
    def test_is_cracked_derives_from_regime(self, regime: Regime, expected: bool) -> None:
        """is_cracked is a derived view on the regime: only SLS_CRACKED reads as cracked."""
        result = StressStrainResult(
            forces=SectionForces(m_y=150.0),
            regime=regime,
            concrete_stress_min=-7.5,
            concrete_stress_max=2.0,
            rebar_results=[],
            raw=None,
        )
        assert result.is_cracked is expected

    def test_cracked_properties_default_none(self) -> None:
        """An uncracked result carries no cracked properties by default."""
        assert self._result(raw=_FakeRaw()).cracked_properties is None

    def test_plot_mesh_stress_delegates_to_backend(self) -> None:
        """plot_mesh_stress() forwards its arguments to the backend's plot_stress and returns its result."""
        raw = _FakeRaw()
        result = self._result(raw=raw)
        returned = result.plot_mesh_stress("a", keyword=1)
        assert returned == "plotted"
        assert raw.calls == [(("a",), {"keyword": 1})]

    def test_plot_without_strain_plane_raises(self) -> None:
        """plot() needs an analyzer-produced result (strain plane + geometry); a bare result raises."""
        with pytest.raises(ValueError, match="analyzer"):
            self._result(raw=_FakeRaw()).plot()


class TestStrainPlane:
    """Tests for StrainPlane (pure arithmetic, no backend)."""

    def test_stores_fields(self) -> None:
        """All fields are stored as given."""
        plane = StrainPlane(eps_0=0.5, kappa_y=-4.0e-6, kappa_z=0.0, neutral_axis_depth=126.4, neutral_axis_angle=0.0)
        assert (plane.eps_0, plane.kappa_y, plane.kappa_z, plane.neutral_axis_depth, plane.neutral_axis_angle) == (
            0.5,
            -4.0e-6,
            0.0,
            126.4,
            0.0,
        )

    def test_is_frozen(self) -> None:
        """StrainPlane is immutable."""
        plane = StrainPlane(eps_0=0.5, kappa_y=-4.0e-6, kappa_z=0.0, neutral_axis_depth=None, neutral_axis_angle=0.0)
        with pytest.raises(AttributeError):
            plane.eps_0 = 1.0  # type: ignore[misc]

    def test_strain_at_origin_is_eps_0(self) -> None:
        """The strain at the origin equals eps_0."""
        plane = StrainPlane(eps_0=0.5, kappa_y=-4.0e-6, kappa_z=3.0e-6, neutral_axis_depth=None, neutral_axis_angle=0.0)
        assert plane.strain_at(0.0, 0.0) == pytest.approx(0.5)

    def test_strain_at_applies_both_curvatures(self) -> None:
        """strain_at adds the vertical and horizontal gradients, converted from ratio/mm to per mille."""
        plane = StrainPlane(eps_0=1.0, kappa_y=-4.0e-6, kappa_z=2.0e-6, neutral_axis_depth=None, neutral_axis_angle=0.0)
        # 1.0 + (2e-6 * 100 + (-4e-6) * 250) * 1000 = 1.0 + (2e-4 - 1e-3) * 1000 = 1.0 - 0.8 = 0.2
        assert plane.strain_at(100.0, 250.0) == pytest.approx(0.2)


class TestCrackedProperties:
    """Tests for CrackedProperties."""

    def test_stores_fields(self) -> None:
        """All fields are stored as given."""
        properties = CrackedProperties(m_cr=44.0, neutral_axis_depth=126.4, theta=0.0, i_cracked=9.5e8, raw=object())
        assert (properties.m_cr, properties.neutral_axis_depth, properties.theta, properties.i_cracked) == (44.0, 126.4, 0.0, 9.5e8)

    def test_is_frozen(self) -> None:
        """CrackedProperties is immutable."""
        properties = CrackedProperties(m_cr=44.0, neutral_axis_depth=126.4, theta=0.0, i_cracked=9.5e8, raw=object())
        with pytest.raises(AttributeError):
            properties.m_cr = 0.0  # type: ignore[misc]
