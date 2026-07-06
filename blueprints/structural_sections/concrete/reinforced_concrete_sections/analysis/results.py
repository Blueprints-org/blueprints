"""Frozen result objects for reinforced-concrete cross-section analysis.

All values are in Blueprints conventions and units: stresses and strains are **compression negative /
tension positive**, consistent with section forces where a positive normal force is tension.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.plotting import (
    plot_biaxial_diagram,
    plot_interaction_diagram,
    plot_moment_curvature,
    plot_stress_strain,
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
        """Plot the strain and stress diagrams over the section height (IDEA-RCS style).

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
