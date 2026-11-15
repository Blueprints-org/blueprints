"""Frozen result objects for reinforced-concrete cross-section analysis.

All values are in Blueprints conventions and units: stresses and strains are **compression negative /
tension positive**, consistent with section forces where a positive normal force is tension.
"""

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from itertools import pairwise
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.plotting import (
    plot_biaxial_diagram,
    plot_interaction_diagram,
    plot_interaction_envelope,
    plot_interaction_section,
    plot_interaction_surface,
    plot_moment_curvature,
    plot_stress_strain,
    plot_verification,
)
from blueprints.structural_sections.section_forces import SectionForces
from blueprints.type_alias import DEG, DIMENSIONLESS, KN, KNM, MM, MM4, MPA, ONE_OVER_MM, PER_MILLE, RAD
from blueprints.unit_conversion import RATIO_TO_PER_MILLE


class Regime(Enum):
    """Stress/strain analysis regime.

    ``AUTO`` lets the analyzer decide between the SLS regimes: it runs the (cheap) uncracked analysis
    first and switches to the cracked analysis when the concrete tensile stress exceeds the flexural
    tensile strength f_ctm,fl. The other members force a specific regime. A ``StressStrainResult``
    always carries the concrete regime that actually produced it, never ``AUTO``.
    """

    AUTO = "AUTO"
    SLS_UNCRACKED = "SLS_UNCRACKED"
    SLS_CRACKED = "SLS_CRACKED"
    ULS = "ULS"


@dataclass(frozen=True)
class RebarStressResult:
    """Stress and strain state of a single reinforcement bar.

    Parameters
    ----------
    x : MM
        x-coordinate of the bar centroid in the cross-section plane [mm].
    y : MM
        y-coordinate of the bar centroid in the cross-section plane [mm].
    diameter : MM
        Bar diameter [mm].
    stress : MPA
        Axial stress in the bar, compression negative / tension positive [MPa].
    strain : PER_MILLE
        Axial strain in the bar, compression negative / tension positive [‰].
    force : KN
        Axial force in the bar, compression negative / tension positive [kN].
    """

    x: MM
    y: MM
    diameter: MM
    stress: MPA
    strain: PER_MILLE
    force: KN


@dataclass(frozen=True)
class StrainPlane:
    """Linear strain field over the cross-section (plane sections remain plane).

    The strain at a point ``(x, y)`` in the cross-section plane follows from ``strain_at`` and is
    expressed compression negative / tension positive. ``x`` is the horizontal and ``y`` the vertical
    cross-section coordinate — the same axes as ``Rebar.x`` / ``Rebar.y`` and the section profile.

    Parameters
    ----------
    eps_0 : PER_MILLE
        Strain at the section origin (``x = y = 0``), compression negative / tension positive [‰].
    kappa_y : ONE_OVER_MM
        Curvature about the y-axis: the strain gradient in the vertical (y) direction, as a ratio strain
        per mm [1/mm]. Driven by ``m_y``.
    kappa_z : ONE_OVER_MM
        Curvature about the z-axis: the strain gradient in the horizontal (x) direction, as a ratio
        strain per mm [1/mm]. Driven by ``m_z``.
    neutral_axis_depth : MM | None
        Perpendicular distance from the extreme compression fibre to the zero-strain (neutral) line
        [mm]. ``None`` when the section has no curvature (pure axial) or no fibre in compression.
    neutral_axis_angle : DEG
        Orientation of the neutral (zero-strain) line, measured counter-clockwise from the x-axis and
        normalized to ``[-90, 90)`` [deg]. ``0`` for a horizontal neutral axis (pure ``m_y`` bending) and
        ``0`` by convention when there is no curvature.
    """

    eps_0: PER_MILLE
    kappa_y: ONE_OVER_MM
    kappa_z: ONE_OVER_MM
    neutral_axis_depth: MM | None
    neutral_axis_angle: DEG

    def strain_at(self, x: MM, y: MM) -> PER_MILLE:
        """Return the strain at cross-section point ``(x, y)``.

        Parameters
        ----------
        x : MM
            Horizontal cross-section coordinate [mm].
        y : MM
            Vertical cross-section coordinate [mm].

        Returns
        -------
        PER_MILLE
            Strain at the point, compression negative / tension positive [‰].
        """
        return self.eps_0 + (self.kappa_z * x + self.kappa_y * y) * RATIO_TO_PER_MILLE


@dataclass(frozen=True)
class CrackedProperties:
    """Cracked-section properties of a reinforced-concrete cross-section.

    Parameters
    ----------
    m_cr : KNM
        Cracking moment of the section [kNm].
    neutral_axis_depth : MM
        Depth of the cracked neutral axis from the extreme compression fibre [mm].
    theta : RAD
        Angle of the neutral axis used for the cracked analysis [rad].
    i_cracked : MM4
        Second moment of area of the cracked transformed section about the neutral axis [mm⁴].
    raw : Any
        The underlying backend cracked-results object, kept as an escape hatch for advanced use.
    """

    m_cr: KNM
    neutral_axis_depth: MM
    theta: RAD
    i_cracked: MM4
    raw: Any


@dataclass(frozen=True)
class UltimateCapacityResult:
    """Ultimate (ULS) bending capacity of a reinforced-concrete cross-section at a given axial force.

    The capacity follows from the design materials (f_cd, f_yd) with the strain plane pivoting on the
    concrete crushing strain eps_cu3 at the extreme compression fibre; the neutral-axis depth is iterated
    until the internal axial force balances ``n``.

    Parameters
    ----------
    n : KN
        The axial force at which the capacity was computed, compression negative / tension positive [kN].
    m_y_rd : KNM
        Design bending capacity about the y-axis (Blueprints sign convention: positive tensions the
        bottom fibre) [kNm].
    m_z_rd : KNM
        Design bending capacity about the z-axis [kNm].
    m_rd : KNM
        Resultant design bending capacity, the magnitude of ``(m_y_rd, m_z_rd)`` [kNm].
    neutral_axis_depth : MM
        Ultimate neutral-axis depth from the extreme compression fibre [mm].
    neutral_axis_angle : DEG
        Orientation of the neutral axis, measured counter-clockwise from the section x-axis [deg]. ``0``
        for sagging about the y-axis, ``180`` for hogging.
    k_u : DIMENSIONLESS
        Neutral-axis parameter ``d_n / d`` with ``d`` the effective depth to the extreme tension bar [-].
    raw : Any
        The underlying backend result object, kept as an escape hatch for advanced use.
    """

    n: KN
    m_y_rd: KNM
    m_z_rd: KNM
    m_rd: KNM
    neutral_axis_depth: MM
    neutral_axis_angle: DEG
    k_u: DIMENSIONLESS
    raw: Any


@dataclass(frozen=True)
class InteractionPoint:
    """One (N, M) point of an interaction diagram, in Blueprints conventions.

    Parameters
    ----------
    n : KN
        Axial force, compression negative / tension positive [kN].
    m_y : KNM
        Bending moment component about the y-axis [kNm].
    m_z : KNM
        Bending moment component about the z-axis [kNm].
    m : KNM
        Resultant bending moment, the magnitude of ``(m_y, m_z)`` [kNm].
    label : str | None
        Backend label of a control point (for example the pure-compression point), if any.
    """

    n: KN
    m_y: KNM
    m_z: KNM
    m: KNM
    label: str | None = None


@dataclass(frozen=True)
class MomentInteractionResult:
    """Uniaxial N-M interaction diagram of a reinforced-concrete cross-section (ULS design materials).

    The diagram runs from the pure-compression (squash) point to the zero-curvature tension point for a
    fixed neutral-axis angle ``theta``. Each point is an ultimate capacity at a different axial force.

    Parameters
    ----------
    theta : DEG
        The neutral-axis angle of the diagram, measured counter-clockwise from the section x-axis
        [deg]. ``0`` for sagging about the y-axis.
    points : tuple[InteractionPoint, ...]
        The (N, M) points of the diagram, in Blueprints conventions.
    raw : Any
        The underlying backend result object, kept as an escape hatch for advanced use.
    """

    theta: DEG
    points: tuple[InteractionPoint, ...]
    raw: Any

    def plot(self, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
        """Plot the N-M interaction diagram (M on the x-axis, N on the y-axis, tension positive).

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the interaction diagram.
        """
        return plot_interaction_diagram(self, figsize=figsize)


@dataclass(frozen=True)
class MomentInteractionEnvelope:
    """Closed uniaxial N-M interaction envelope about a single bending axis (ULS design materials).

    Where :class:`MomentInteractionResult` traces a single neutral-axis angle — one side of the
    envelope — this stitches the positive- and negative-moment branches into one closed curve, the
    familiar closed "N-M resultant" interaction envelope. The plotted moment carries its
    sign, so an asymmetrically reinforced section shows its two different capacities: a section with
    only bottom reinforcement has a large sagging (positive) and a small hogging (negative) capacity,
    and the loop makes that asymmetry visible instead of mirroring one branch onto the other.

    Parameters
    ----------
    axis : str
        The bending axis the envelope is drawn about: ``"y"`` (sagging/hogging, the signed moment is
        ``m_y``) or ``"z"`` (the signed moment is ``m_z``).
    points : tuple[InteractionPoint, ...]
        The (N, M) points of the closed loop in Blueprints conventions, ordered around the envelope
        with the first point repeated at the end. The moment component matching ``axis`` carries the
        sign; the other component is zero.
    raw : Any
        The two underlying backend results ``(positive, negative)`` as a tuple, kept as an escape hatch
        for advanced use.
    """

    axis: str
    points: tuple[InteractionPoint, ...]
    raw: Any

    @classmethod
    def from_branches(cls, positive: "MomentInteractionResult", negative: "MomentInteractionResult", *, axis: str) -> "MomentInteractionEnvelope":
        """Stitch a positive- and a negative-moment branch into one closed envelope.

        Both branches run from the pure-compression (squash) point to the pure-tension point, which
        they share: at the axial extremes the curvature vanishes so the neutral-axis angle is
        irrelevant and the endpoints coincide. The positive branch is kept as traced (squash to
        tension); the negative branch is reversed and its two shared endpoints dropped, then the loop is
        closed back onto the squash point.

        Parameters
        ----------
        positive : MomentInteractionResult
            The positive-moment branch (for example ``theta=0`` about the y-axis).
        negative : MomentInteractionResult
            The negative-moment branch (for example ``theta=180`` about the y-axis).
        axis : str
            The bending axis of the envelope, ``"y"`` or ``"z"``.

        Returns
        -------
        MomentInteractionEnvelope
            The closed envelope.
        """
        forward = list(positive.points)
        interior = list(reversed(negative.points))[1:-1]  # drop the shared tension and squash endpoints
        points = (*forward, *interior, forward[0])  # close the loop back onto the squash point
        return cls(axis=axis, points=points, raw=(positive.raw, negative.raw))

    def plot(self, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
        """Plot the closed N-M interaction envelope (signed M on the x-axis, N on the y-axis, tension +).

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the closed interaction envelope.
        """
        return plot_interaction_envelope(self, figsize=figsize)


@dataclass(frozen=True)
class BiaxialInteractionResult:
    """Biaxial M_y-M_z interaction envelope at a fixed axial force (ULS design materials).

    The envelope traverses the neutral-axis angle over a full revolution; each point is the ultimate
    bending capacity at that angle for the fixed axial force ``n``.

    Parameters
    ----------
    n : KN
        The fixed axial force of the envelope, compression negative / tension positive [kN].
    points : tuple[InteractionPoint, ...]
        The (M_y, M_z) points of the closed envelope, in Blueprints conventions.
    raw : Any
        The underlying backend result object, kept as an escape hatch for advanced use.
    """

    n: KN
    points: tuple[InteractionPoint, ...]
    raw: Any

    def capacity_along(self, m_y: KNM, m_z: KNM) -> KNM:
        """Resultant bending capacity along the direction of the given moment pair.

        Intersects the envelope with the ray from the origin through ``(m_y, m_z)`` (linear
        interpolation between the envelope points) and returns the resultant capacity at the
        intersection.

        Parameters
        ----------
        m_y : KNM
            Bending moment component about the y-axis setting the direction [kNm].
        m_z : KNM
            Bending moment component about the z-axis setting the direction [kNm].

        Returns
        -------
        KNM
            The resultant bending capacity along the direction of ``(m_y, m_z)`` [kNm].

        Raises
        ------
        ValueError
            If both moment components are zero (no direction), or if the ray does not intersect the
            envelope (a degenerate envelope).
        """
        magnitude = math.hypot(m_y, m_z)
        if magnitude == 0.0:
            raise ValueError("The moment direction is undefined: both m_y and m_z are zero.")
        direction = np.array([m_y, m_z]) / magnitude
        for start, end in zip(self.points[:-1], self.points[1:], strict=True):
            p_start = np.array([start.m_y, start.m_z])
            segment = np.array([end.m_y - start.m_y, end.m_z - start.m_z])
            matrix = np.column_stack([segment, -direction])
            try:
                t, s = np.linalg.solve(matrix, -p_start)
            except np.linalg.LinAlgError:
                continue  # segment parallel to the ray (or degenerate)
            if 0.0 <= t <= 1.0 and s > 0.0:
                return float(s)
        raise ValueError("The load direction does not intersect the biaxial envelope; the envelope appears degenerate.")

    def plot(self, *, figsize: tuple[float, float] = (6.0, 6.0)) -> Figure:
        """Plot the biaxial M_y-M_z interaction envelope.

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the biaxial envelope.
        """
        return plot_biaxial_diagram(self, figsize=figsize)


def _axial_range(meridians: "Sequence[MomentInteractionResult]") -> tuple[KN, KN]:
    """Axial range covered by every meridian: ``(n_min, n_max)`` with no meridian extrapolated.

    The meridians share their squash and pure-tension poles, so this range is common to all of them; it
    is derived from the meridians (not from a separate squash/tension estimate) so a ring at any level in
    the range can be interpolated from every meridian without extrapolation.
    """
    n_min = max(min(point.n for point in meridian.points) for meridian in meridians)
    n_max = min(max(point.n for point in meridian.points) for meridian in meridians)
    return n_min, n_max


def _interpolate_ring(meridians: "Sequence[MomentInteractionResult]", n: KN) -> tuple["InteractionPoint", ...]:
    """Interpolate every meridian at a fixed axial force to build the closed fixed-N ring.

    Each meridian is a full N-sweep at a fixed neutral-axis angle; sampling them all at the same axial
    force ``n`` gives one moment point per angle, and the ordered set over the angles is the closed
    (M_y, M_z) ring at that axial force. The first vertex is repeated at the end to close the loop.
    """
    ring: list[InteractionPoint] = []
    for meridian in meridians:
        points = sorted(meridian.points, key=lambda point: point.n)  # np.interp needs an increasing axial abscissa
        axial = [point.n for point in points]
        m_y = float(np.interp(n, axial, [point.m_y for point in points]))
        m_z = float(np.interp(n, axial, [point.m_z for point in points]))
        ring.append(InteractionPoint(n=n, m_y=m_y, m_z=m_z, m=math.hypot(m_y, m_z)))
    ring.append(ring[0])  # close the ring
    return tuple(ring)


def _line_section(ring: "Sequence[InteractionPoint]", u_y: float, u_z: float) -> tuple[KNM, KNM] | None:
    """Extreme signed projections onto ``u`` where the line through the origin along ``u`` crosses the ring.

    The line (not a ray) through the origin in the unit direction ``u`` cuts the closed (M_y, M_z) ring;
    each crossing is projected onto ``u`` as a signed scalar. The most positive and most negative
    projections are the two boundaries of the resultant section at this axial level. ``None`` is returned
    when the line does not cross the ring (fewer than two crossings), which happens near the poles where a
    ring shrinks to a point offset from the origin.

    Parameters
    ----------
    ring : Sequence[InteractionPoint]
        The closed fixed-N ring (first vertex repeated at the end).
    u_y : float
        y-component of the unit moment direction.
    u_z : float
        z-component of the unit moment direction.

    Returns
    -------
    tuple[KNM, KNM] | None
        ``(t_max, t_min)`` signed projections [kNm], or ``None`` when the line misses the ring.
    """
    normal_y, normal_z = -u_z, u_y  # normal to the direction; a crossing is a sign change of the signed distance
    projections: list[float] = []
    for start, end in pairwise(ring):
        distance_start = start.m_y * normal_y + start.m_z * normal_z
        distance_end = end.m_y * normal_y + end.m_z * normal_z
        if (distance_start >= 0.0) == (distance_end >= 0.0):
            continue  # both vertices on the same side of the line: no crossing on this edge
        fraction = distance_start / (distance_start - distance_end)
        crossing_y = start.m_y + fraction * (end.m_y - start.m_y)
        crossing_z = start.m_z + fraction * (end.m_z - start.m_z)
        projections.append(crossing_y * u_y + crossing_z * u_z)
    if len(projections) < 2:
        return None
    return max(projections), min(projections)


def _component_section(ring: "Sequence[InteractionPoint]", *, free_y: bool, fixed_value: KNM) -> tuple[KNM, KNM] | None:
    """Extreme free-component moments where the ring crosses the line at ``fixed_value`` on the other component.

    For ``free_y=True`` the cutting line is ``M_z = fixed_value`` and the returned extremes are the ``M_y``
    values there; for ``free_y=False`` the line is ``M_y = fixed_value`` and the extremes are ``M_z``.
    ``None`` is returned when the line does not cross the ring (fewer than two crossings), which happens at
    axial levels where the ring does not reach ``fixed_value`` on the fixed component.

    Parameters
    ----------
    ring : Sequence[InteractionPoint]
        The closed fixed-N ring (first vertex repeated at the end).
    free_y : bool
        Whether ``M_y`` is the free component (line at constant ``M_z``) or ``M_z`` is (line at constant ``M_y``).
    fixed_value : KNM
        The value of the fixed component defining the cutting line [kNm].

    Returns
    -------
    tuple[KNM, KNM] | None
        ``(free_max, free_min)`` extreme free-component moments [kNm], or ``None`` when the line misses the ring.
    """
    values: list[float] = []
    for start, end in pairwise(ring):
        fixed_start = (start.m_z if free_y else start.m_y) - fixed_value
        fixed_end = (end.m_z if free_y else end.m_y) - fixed_value
        if (fixed_start >= 0.0) == (fixed_end >= 0.0):
            continue  # both vertices on the same side of the line: no crossing on this edge
        fraction = fixed_start / (fixed_start - fixed_end)
        free_start = start.m_y if free_y else start.m_z
        free_end = end.m_y if free_y else end.m_z
        values.append(free_start + fraction * (free_end - free_start))
    if len(values) < 2:
        return None
    return max(values), min(values)


@dataclass(frozen=True)
class InteractionSection:
    """A planar N-M section through the interaction surface (design materials).

    The section is the intersection of the ULS capacity surface with a vertical plane through the axial
    (N) axis; three cut kinds are supported, and the cutting plane is fixed by the design forces, so the
    section's shape depends on them:

    - ``"resultant"`` — the plane containing the N-axis and the moment **direction** of ``fixed``; the
      plotted moment is the signed resultant projected onto that direction (the closed "N-M resultant"
      diagram cut along an applied moment).
    - ``"n_my"`` — the plane ``M_z = fixed[1]``; the plotted moment is the signed ``M_y``.
    - ``"n_mz"`` — the plane ``M_y = fixed[0]``; the plotted moment is the signed ``M_z``.

    Parameters
    ----------
    kind : str
        The cut kind: ``"resultant"``, ``"n_my"`` or ``"n_mz"``.
    fixed : tuple[KNM, KNM]
        The moment pair defining the cut: a direction for ``"resultant"``; the pinned component for
        ``"n_my"``/``"n_mz"`` (the free component's slot is zero) [kNm].
    points : tuple[InteractionPoint, ...]
        The (N, M) points of the closed loop in Blueprints conventions, ordered around the section with
        the first point repeated at the end. :meth:`signed_moments` gives the signed moment used for
        plotting.
    raw : Any
        Escape hatch for advanced use; ``None`` for a section built from an interpolated surface.
    """

    kind: str
    fixed: tuple[KNM, KNM]
    points: tuple[InteractionPoint, ...]
    raw: Any

    @property
    def direction(self) -> tuple[float, float]:
        """Unit ``(u_y, u_z)`` moment direction of the cutting plane (meaningful for a resultant section)."""
        m_y, m_z = self.fixed
        magnitude = math.hypot(m_y, m_z)
        return m_y / magnitude, m_z / magnitude

    def signed_moments(self) -> list[KNM]:
        """Signed moment of each point on the section's plotted axis [kNm].

        The resultant projection for a ``"resultant"`` section, the signed ``M_y`` for ``"n_my"`` and the
        signed ``M_z`` for ``"n_mz"``.
        """
        if self.kind == "n_my":
            return [point.m_y for point in self.points]
        if self.kind == "n_mz":
            return [point.m_z for point in self.points]
        u_y, u_z = self.direction
        return [point.m_y * u_y + point.m_z * u_z for point in self.points]

    def plot(self, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
        """Plot the closed N-M section (signed M on the x-axis, N on the y-axis, tension +).

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the closed section.
        """
        return plot_interaction_section(self, figsize=figsize)


@dataclass(frozen=True)
class InteractionSurface:
    """ULS capacity surface in (N, M_y, M_z), sampled as neutral-axis-angle meridians (design materials).

    The surface is the general parent of the fixed-neutral-axis-angle diagram (:class:`MomentInteractionResult`)
    and the fixed-axial-force envelope (:class:`BiaxialInteractionResult`): it is sampled as a set of
    meridians, one uniaxial N-M diagram per neutral-axis angle over a full revolution. Any planar section
    is sliced from it — a fixed-axial-force ring via :meth:`ring`, or a fixed-direction N-M resultant
    section via :meth:`section_resultant`.

    The slicing uses linear interpolation between meridians and along the axial force, so the surface is a
    visualization tool; the governing unity check stays on the exact capacity routines
    (:meth:`~...CrossSectionAnalysis.bending_capacity`, :meth:`~...CrossSectionAnalysis.biaxial_interaction`).

    Parameters
    ----------
    thetas : tuple[DEG, ...]
        The neutral-axis angles of the meridians over ``[0, 360)`` [deg].
    meridians : tuple[MomentInteractionResult, ...]
        One uniaxial N-M diagram per angle in ``thetas`` (the raw backend samples).
    raw : Any
        Escape hatch for advanced use.
    """

    thetas: tuple[DEG, ...]
    meridians: tuple[MomentInteractionResult, ...]
    raw: Any

    def ring(self, n: KN) -> "BiaxialInteractionResult":
        """The fixed-axial-force M_y-M_z ring, interpolated from the meridians at axial force ``n``.

        Parameters
        ----------
        n : KN
            The axial force, compression negative / tension positive [kN]. Must lie within the surface's
            axial range.

        Returns
        -------
        BiaxialInteractionResult
            The closed M_y-M_z ring at ``n``, with the same interface as :meth:`biaxial_interaction`.

        Raises
        ------
        ValueError
            If ``n`` lies outside the axial range covered by every meridian.
        """
        n_min, n_max = _axial_range(self.meridians)
        if not n_min <= n <= n_max:
            raise ValueError(f"The axial force {n} kN is outside the surface's axial range [{n_min:.0f}, {n_max:.0f}] kN.")
        return BiaxialInteractionResult(n=n, points=_interpolate_ring(self.meridians, n), raw=None)

    def section_resultant(self, *, m_y: KNM, m_z: KNM, n_levels: int = 48) -> InteractionSection:
        """Slice the closed N-M resultant section along the direction of the moment pair ``(m_y, m_z)``.

        For each of ``n_levels`` axial forces the fixed-N ring is intersected with the line through the
        origin along the moment direction, giving the resultant capacity on both sides; stacking those
        boundaries closes the section into a loop. Axial levels whose ring the line does not reach (near
        the poles, where the ring shrinks to a point offset from the origin) are skipped.

        Parameters
        ----------
        m_y : KNM
            y-component of the moment whose direction sets the cutting plane [kNm].
        m_z : KNM
            z-component of the moment whose direction sets the cutting plane [kNm].
        n_levels : int
            Number of axial levels sampled across the surface's axial range.

        Returns
        -------
        InteractionSection
            The closed N-M resultant section along ``(m_y, m_z)``.

        Raises
        ------
        ValueError
            If both moment components are zero (no direction), or if the direction does not intersect the
            surface at any axial level.
        """
        magnitude = math.hypot(m_y, m_z)
        if magnitude == 0.0:
            raise ValueError("The moment direction is undefined: both m_y and m_z are zero.")
        u_y, u_z = m_y / magnitude, m_z / magnitude

        def slicer(ring: tuple[InteractionPoint, ...]) -> tuple[KNM, KNM] | None:
            return _line_section(ring, u_y, u_z)

        def point(n: KN, t: KNM) -> InteractionPoint:  # the crossing lies on the direction line, so it is t * u
            return InteractionPoint(n=n, m_y=t * u_y, m_z=t * u_z, m=abs(t))

        return self._build_section("resultant", (m_y, m_z), slicer, point, n_levels)

    def section_n_my(self, *, m_z: KNM = 0.0, n_levels: int = 48) -> InteractionSection:
        """Slice the closed N-M_y section at a fixed transverse moment ``M_z``.

        For each of ``n_levels`` axial forces the fixed-N ring is intersected with the line ``M_z = m_z``,
        giving the M_y capacity on both sides; stacking those boundaries closes the section into a loop.
        ``m_z=0`` is the section through the symmetry plane; a non-zero ``m_z`` narrows the loop. Axial
        levels whose ring does not reach ``M_z = m_z`` are skipped.

        Parameters
        ----------
        m_z : KNM
            The fixed transverse moment defining the cutting plane [kNm].
        n_levels : int
            Number of axial levels sampled across the surface's axial range.

        Returns
        -------
        InteractionSection
            The closed N-M_y section at ``M_z = m_z``.

        Raises
        ------
        ValueError
            If the plane ``M_z = m_z`` does not intersect the surface at any axial level.
        """

        def slicer(ring: tuple[InteractionPoint, ...]) -> tuple[KNM, KNM] | None:
            return _component_section(ring, free_y=True, fixed_value=m_z)

        def point(n: KN, m_y: KNM) -> InteractionPoint:
            return InteractionPoint(n=n, m_y=m_y, m_z=m_z, m=math.hypot(m_y, m_z))

        return self._build_section("n_my", (0.0, m_z), slicer, point, n_levels)

    def section_n_mz(self, *, m_y: KNM = 0.0, n_levels: int = 48) -> InteractionSection:
        """Slice the closed N-M_z section at a fixed moment ``M_y``.

        For each of ``n_levels`` axial forces the fixed-N ring is intersected with the line ``M_y = m_y``,
        giving the M_z capacity on both sides; stacking those boundaries closes the section into a loop.
        Axial levels whose ring does not reach ``M_y = m_y`` are skipped (near the poles the ring is
        offset off that line, so the loop narrows and closes).

        Parameters
        ----------
        m_y : KNM
            The fixed moment defining the cutting plane [kNm].
        n_levels : int
            Number of axial levels sampled across the surface's axial range.

        Returns
        -------
        InteractionSection
            The closed N-M_z section at ``M_y = m_y``.

        Raises
        ------
        ValueError
            If the plane ``M_y = m_y`` does not intersect the surface at any axial level.
        """

        def slicer(ring: tuple[InteractionPoint, ...]) -> tuple[KNM, KNM] | None:
            return _component_section(ring, free_y=False, fixed_value=m_y)

        def point(n: KN, m_z: KNM) -> InteractionPoint:
            return InteractionPoint(n=n, m_y=m_y, m_z=m_z, m=math.hypot(m_y, m_z))

        return self._build_section("n_mz", (m_y, 0.0), slicer, point, n_levels)

    def plot_3d(self, *, figsize: tuple[float, float] = (7.0, 6.0), n_levels: int = 24) -> Figure:
        """Plot the interaction surface in 3D as (M_y, M_z, N), with the axial force on the vertical axis.

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.
        n_levels : int
            Number of axial rings sampled across the surface's axial range.

        Returns
        -------
        Figure
            The matplotlib figure with the 3D interaction surface.
        """
        return plot_interaction_surface(self, figsize=figsize, n_levels=n_levels)

    def _build_section(
        self,
        kind: str,
        fixed: tuple[KNM, KNM],
        slicer: Callable[[tuple["InteractionPoint", ...]], tuple[KNM, KNM] | None],
        point: Callable[[KN, KNM], "InteractionPoint"],
        n_levels: int,
    ) -> "InteractionSection":
        """Stack the per-ring slice extremes across the axial range into one closed section loop.

        ``slicer`` returns the ``(high, low)`` extreme moments where a ring is cut, and ``point`` maps a
        ``(n, extreme)`` pair to an interaction point; axial levels the slicer misses are skipped. The
        loop runs up one boundary and down the other, closed by repeating the first point.
        """
        n_min, n_max = _axial_range(self.meridians)
        upper: list[InteractionPoint] = []
        lower: list[InteractionPoint] = []
        for n in np.linspace(n_min, n_max, n_levels):
            extremes = slicer(_interpolate_ring(self.meridians, float(n)))
            if extremes is None:
                continue
            high, low = extremes
            upper.append(point(float(n), high))
            lower.append(point(float(n), low))
        if not upper:
            raise ValueError("The cutting plane does not intersect the interaction surface at any axial level.")
        return InteractionSection(kind=kind, fixed=fixed, points=(*upper, *reversed(lower), upper[0]), raw=None)


@dataclass(frozen=True)
class UtilizationResult:
    """Unity check of a ULS design action against the section's design capacity.

    The bending capacity is evaluated at the design axial force (accounting for N-M interaction) and
    along the design moment direction, so the utilization is the ratio of the resultant design moment
    to the capacity in the same direction. A pure axial action is checked against the squash or tensile
    capacity instead.

    Parameters
    ----------
    forces : SectionForces
        The design action that was verified (echoed back for traceability).
    utilization : DIMENSIONLESS
        The unity check value: <= 1 means the design action fits within the capacity [-].
    governing : str
        The governing check: ``"axial"``, ``"uniaxial bending"`` or ``"biaxial bending"``.
    n_rd : KN | None
        The axial capacity in the direction of the design axial force (squash negative, tensile
        positive) [kN]; ``None`` when there is no axial force.
    m_ed : KNM
        The resultant design bending moment [kNm].
    m_rd : KNM | None
        The resultant bending capacity at the design axial force, along the design moment direction
        [kNm]; ``None`` for a pure axial check or when the axial force already exceeds its capacity.
    """

    forces: SectionForces
    utilization: DIMENSIONLESS
    governing: str
    n_rd: KN | None
    m_ed: KNM
    m_rd: KNM | None

    @property
    def is_ok(self) -> bool:
        """Whether the design action fits within the design capacity (utilization <= 1)."""
        return self.utilization <= 1.0


@dataclass(frozen=True)
class VerificationDiagram:
    """A ULS unity check drawn on the capacity section along the design action's moment direction.

    Combines the resultant capacity section (the closed N-M loop cut along the design moment direction)
    with the unity-check numbers, so the plot shows the design action and the capacity as two markers on
    the same axes with the utilization. The capacity marker is taken from the exact check
    (:meth:`~...CrossSectionAnalysis.verify`), while the loop comes from the interpolated surface, so the
    marker may sit marginally off the drawn loop.

    Parameters
    ----------
    section : InteractionSection
        The resultant capacity section along the design moment direction.
    utilization : UtilizationResult
        The unity-check result providing the design action, the capacity and the utilization; it always
        carries a bending capacity (``m_rd`` is not ``None``).
    """

    section: InteractionSection
    utilization: UtilizationResult

    def plot(self, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
        """Plot the capacity section with the design-action and capacity markers and the utilization.

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the capacity section and the unity-check markers.
        """
        return plot_verification(self, figsize=figsize)


@dataclass(frozen=True)
class MomentCurvatureResult:
    """Moment-curvature response of a reinforced-concrete cross-section at a fixed axial force.

    The curve is computed with the design material set (concrete bilinear-horizontal at f_cd with a
    tension branch up to f_ctm,fl, reinforcement at f_yd) and runs from zero curvature up to material
    failure (concrete crushing or steel fracture). The cracking kink, the reinforcement yield point and
    the ultimate moment are all part of the traced curve.

    Parameters
    ----------
    theta : DEG
        The neutral-axis angle of the analysis, measured counter-clockwise from the section x-axis
        [deg].
    n : KN
        The fixed axial force, compression negative / tension positive [kN].
    kappa : tuple[ONE_OVER_MM, ...]
        The curvature steps [1/mm].
    m_y : tuple[KNM, ...]
        Bending moment component about the y-axis at each step [kNm].
    m_z : tuple[KNM, ...]
        Bending moment component about the z-axis at each step [kNm].
    m : tuple[KNM, ...]
        Resultant bending moment at each step, the magnitude of ``(m_y, m_z)`` [kNm].
    raw : Any
        The underlying backend result object (including the failed-material geometry), kept as an
        escape hatch for advanced use.
    tension_stiffening : bool
        Whether the curvatures carry the tension-stiffening interpolation of EN 1992-1-1 art. 7.4.3
        (``kappa`` is then the mean curvature between cracks, stiffer than the bare cracked response).
    """

    theta: DEG
    n: KN
    kappa: tuple[ONE_OVER_MM, ...]
    m_y: tuple[KNM, ...]
    m_z: tuple[KNM, ...]
    m: tuple[KNM, ...]
    raw: Any
    tension_stiffening: bool = False

    @property
    def m_ultimate(self) -> KNM:
        """The ultimate (peak) resultant moment of the traced curve [kNm]."""
        return max(self.m)

    def plot(self, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
        """Plot the moment-curvature curve with the ultimate point marked.

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the moment-curvature curve.
        """
        return plot_moment_curvature(self, figsize=figsize)


@dataclass(frozen=True)
class StressStrainResult:
    """Result of a reinforced-concrete cross-section stress/strain analysis.

    Parameters
    ----------
    forces : SectionForces
        The section forces that produced this result (echoed back for traceability).
    regime : Regime
        The regime that actually produced the result (``SLS_UNCRACKED``, ``SLS_CRACKED`` or ``ULS``,
        never ``AUTO``). Single source of truth for the regime; :attr:`is_cracked` derives from it.
    concrete_stress_min : MPA
        Most compressive concrete stress (algebraic minimum), compression negative [MPa].
    concrete_stress_max : MPA
        Most tensile concrete stress (algebraic maximum), compression negative [MPa].
    rebar_results : Sequence[RebarStressResult]
        Per-bar stress/strain results.
    raw : Any
        The underlying backend result object, kept as an escape hatch for advanced use.
    cracked_properties : CrackedProperties | None
        The cracked-section properties for an ``SLS_CRACKED`` result; ``None`` otherwise.
    strain_plane : StrainPlane | None
        The reconstructed linear strain field over the section. Always populated by the analyzer; the
        default ``None`` exists only for lightweight construction in tests.
    elastic_modulus : MPA
        The concrete elastic modulus used for the analysis — e_cm, or the effective modulus
        e_cm / (1 + phi) when a creep coefficient was given — needed by :meth:`plot` to turn the
        strain profile into a concrete-stress profile [MPa].
    geometry : Any
        The section profile polygon (shapely ``Polygon``), used by :meth:`plot` to draw the section
        panel. Always populated by the analyzer; the default ``None`` exists only for lightweight
        construction in tests.
    concrete_profile : Any
        The backend concrete stress-strain profile for a non-linear (ULS) result, used by :meth:`plot`
        to turn the strain profile into the design stress block; ``None`` for the linear SLS regimes.
    """

    forces: SectionForces
    regime: Regime
    concrete_stress_min: MPA
    concrete_stress_max: MPA
    rebar_results: Sequence[RebarStressResult]
    raw: Any
    cracked_properties: CrackedProperties | None = None
    strain_plane: StrainPlane | None = None
    elastic_modulus: MPA = 0.0
    geometry: Any = None
    concrete_profile: Any = None

    @property
    def is_cracked(self) -> bool:
        """Whether the cracked SLS regime produced this result (derived from :attr:`regime`)."""
        return self.regime is Regime.SLS_CRACKED

    def plot(self, *, figsize: tuple[float, float] = (11.0, 6.0)) -> Figure:
        """Plot the strain and stress diagrams over the section height.

        Draws three panels sharing the section-height axis: the section with its reinforcement, the
        linear strain profile (‰, compression negative), and the stress profile (MPa, compression
        negative) with the reinforcement stresses marked. The profiles are projected onto the axis
        perpendicular to the neutral axis, so uniaxial and biaxial-uncracked states both render upright.

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the three panels.

        Raises
        ------
        ValueError
            If the result was constructed without a strain plane or section geometry (an analyzer always
            supplies both).
        """
        return plot_stress_strain(self, figsize=figsize)

    def plot_mesh_stress(self, *args: object, **kwargs: object) -> Axes:
        """Plot the backend's 2D mesh stress contour, delegating to the backend's stress plot.

        This is the ``concreteproperties`` mesh-contour view (a colour-mapped cross-section), kept
        available under its own name so :meth:`plot` can produce the strain/stress-over-height figure.

        Parameters
        ----------
        *args : object
            Positional arguments forwarded to the backend plotter.
        **kwargs : object
            Keyword arguments forwarded to the backend plotter.

        Returns
        -------
        Axes
            The matplotlib axes produced by the backend plotter.
        """
        return self.raw.plot_stress(*args, **kwargs)
