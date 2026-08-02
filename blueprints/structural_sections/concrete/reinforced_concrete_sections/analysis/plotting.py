"""Strain/stress-over-height plotting for reinforced-concrete section results.

Draws three panels sharing the section-height axis: the section with its reinforcement, the linear
strain profile and the stress profile. The height axis is the direction perpendicular to the neutral
axis (the strain gradient), so uniaxial and biaxial-uncracked states both render upright without special
casing. Everything is in Blueprints conventions: strain in ‰ and stress in MPa, both compression
negative / tension positive.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.patches import Rectangle

from blueprints.type_alias import MPA
from blueprints.unit_conversion import PER_MILLE_TO_RATIO

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import (
        BiaxialInteractionResult,
        InteractionSection,
        InteractionSurface,
        MomentCurvatureResult,
        MomentInteractionEnvelope,
        MomentInteractionResult,
        StrainPlane,
        StressStrainResult,
        VerificationDiagram,
    )

# Strain gradient (ratio/mm) below which the section is treated as having no neutral axis (pure axial).
_CURVATURE_TOL: float = 1e-12
_N_SAMPLES: int = 100

_CONCRETE_FACE = "lightgrey"
_REBAR_COLOUR = "saddlebrown"
_STRAIN_COLOUR = "tab:blue"
_STRESS_COLOUR = "tab:red"
_NEUTRAL_AXIS_COLOUR = "green"
_COMPRESSION_HATCH = "grey"

# Axis-label symbols kept as chr() so the source stays ASCII (avoids ambiguous-unicode lint in string literals).
_EPSILON = chr(0x03B5)  # ε
_SIGMA = chr(0x03C3)  # σ
_PER_MILLE = chr(0x2030)  # ‰
_THETA = chr(0x03B8)  # θ
_DEGREE = chr(0x00B0)  # °
_KAPPA = chr(0x03BA)  # κ


def _projection_axes(plane: StrainPlane) -> tuple[np.ndarray, np.ndarray]:
    """Return the unit height axis (along the strain gradient) and the in-plane axis perpendicular to it.

    The height axis is oriented to point roughly "up" (positive y component) so the section is drawn
    upright. For a flat strain plane (pure axial) it falls back to the geometric vertical.

    Parameters
    ----------
    plane : StrainPlane
        The reconstructed strain plane.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        ``(height_axis, across_axis)`` unit vectors in cross-section (x, y).
    """
    gradient = np.array([plane.kappa_z, plane.kappa_y], dtype=float)  # d(strain)/dx, d(strain)/dy
    magnitude = math.hypot(*gradient)
    if magnitude <= _CURVATURE_TOL:
        height_axis = np.array([0.0, 1.0])
    else:
        height_axis = gradient / magnitude
        if height_axis[1] < 0 or (height_axis[1] == 0 and height_axis[0] < 0):
            height_axis = -height_axis  # orient roughly upward for an upright section
    across_axis = np.array([-height_axis[1], height_axis[0]])
    return height_axis, across_axis


def _concrete_stress(strain_per_mille: np.ndarray, elastic_modulus: MPA, *, is_cracked: bool, profile: object | None = None) -> np.ndarray:
    """Concrete stress from strain: the SLS linear law, or a backend design profile when given.

    Parameters
    ----------
    strain_per_mille : np.ndarray
        Strain samples [‰], compression negative.
    elastic_modulus : MPA
        The concrete elastic modulus (e_cm or E_c,eff) [MPa], used by the linear SLS law.
    is_cracked : bool
        Whether the concrete tension stress must be dropped (cracked SLS regime).
    profile : object | None
        A backend concrete stress-strain profile (compression positive) for a non-linear (ULS) result;
        overrides the linear law when given.

    Returns
    -------
    np.ndarray
        Concrete stress samples [MPa], compression negative.
    """
    if profile is not None:
        # backend profiles are compression-positive: negate the strain in, negate the stress out.
        return np.array([-profile.get_stress(-strain * PER_MILLE_TO_RATIO) for strain in strain_per_mille])  # ty: ignore[unresolved-attribute]
    stress = elastic_modulus * strain_per_mille * PER_MILLE_TO_RATIO
    if is_cracked:
        stress = np.where(stress < 0.0, stress, 0.0)
    return stress


def plot_stress_strain(result: StressStrainResult, *, figsize: tuple[float, float] = (11.0, 6.0)) -> Figure:
    """Plot the strain and stress diagrams over the section height for a stress/strain result.

    Parameters
    ----------
    result : StressStrainResult
        The analysis result. Must carry a strain plane and section geometry (an analyzer supplies both).
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the section, strain and stress panels.

    Raises
    ------
    ValueError
        If the result has no strain plane or no section geometry.
    """
    plane = result.strain_plane
    if plane is None or result.geometry is None or result.elastic_modulus <= 0:
        raise ValueError(
            "Plotting requires a result produced by the analyzer (with a strain plane, section geometry and a positive elastic modulus)."
        )

    height_axis, across_axis = _projection_axes(plane)
    exterior = np.array(result.geometry.exterior.coords, dtype=float)
    heights = exterior @ height_axis
    across = exterior @ across_axis
    h_min, h_max = float(heights.min()), float(heights.max())

    hs = np.linspace(h_min, h_max, _N_SAMPLES)
    sample_points = np.outer(hs, height_axis)  # points along the height axis at across = 0
    strain = np.array([plane.strain_at(px, py) for px, py in sample_points])  # ‰
    stress = _concrete_stress(strain, result.elastic_modulus, is_cracked=result.is_cracked, profile=result.concrete_profile)

    fig, (ax_section, ax_strain, ax_stress) = plt.subplots(1, 3, figsize=figsize, sharey=True, gridspec_kw={"width_ratios": [1.0, 1.3, 1.3]})

    _draw_section(ax_section, across, heights, strain, hs, result, across_axis, height_axis)
    _draw_strain(ax_strain, strain, hs, result, height_axis)
    _draw_stress(ax_stress, stress, hs, result, height_axis)
    _draw_neutral_axis((ax_section, ax_strain, ax_stress), strain, hs)

    regime = {"SLS_UNCRACKED": "uncracked", "SLS_CRACKED": "cracked", "ULS": "ULS"}[result.regime.value]
    fig.suptitle(f"Strain & stress over height - {regime}", fontsize=11)
    fig.tight_layout()
    return fig


def plot_interaction_diagram(result: MomentInteractionResult, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
    """Plot a uniaxial N-M interaction diagram (M on the x-axis, N on the y-axis, tension positive).

    Parameters
    ----------
    result : MomentInteractionResult
        The interaction diagram result.
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the interaction diagram.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([point.m for point in result.points], [point.n for point in result.points], "-o", ms=3, color=_STRESS_COLOUR)
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.set_xlabel("$M_{Rd}$ [kNm]")
    ax.set_ylabel("$N_{Rd}$ [kN]  (tension +)")
    ax.set_title(f"N-M interaction diagram ({_THETA} = {result.theta:g}{_DEGREE})")
    ax.invert_yaxis()  # compression (negative) on top, tension (positive) below
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_interaction_envelope(result: MomentInteractionEnvelope, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
    """Plot a closed uniaxial N-M interaction envelope (signed M on the x-axis, N on the y-axis, tension +).

    Unlike :func:`plot_interaction_diagram`, which plots the resultant (unsigned) moment of a single
    branch, this plots the signed moment component of the envelope's bending axis, so the positive- and
    negative-moment sides close into one loop.

    Parameters
    ----------
    result : MomentInteractionEnvelope
        The closed interaction envelope.
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the closed interaction envelope.
    """
    moments = [point.m_y if result.axis == "y" else point.m_z for point in result.points]
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(moments, [point.n for point in result.points], "-o", ms=3, color=_STRESS_COLOUR)
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.set_xlabel(f"$M_{{{result.axis},Rd}}$ [kNm]")
    ax.set_ylabel("$N_{Rd}$ [kN]  (tension +)")
    ax.set_title(f"N-M interaction envelope (about the {result.axis}-axis)")
    ax.invert_yaxis()  # compression (negative) on top, tension (positive) below
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def _section_labels(result: InteractionSection) -> tuple[str, str]:
    """The x-axis label and title for a planar N-M section, per its cut kind."""
    m_y, m_z = result.fixed
    if result.kind == "n_my":
        return "$M_{y,Rd}$ [kNm]", f"N-$M_y$ section ($M_z$ = {m_z:g} kNm)"
    if result.kind == "n_mz":
        return "$M_{z,Rd}$ [kNm]", f"N-$M_z$ section ($M_y$ = {m_y:g} kNm)"
    angle = math.degrees(math.atan2(m_z, m_y))
    return "$M_{Rd}$ [kNm]", f"N-M resultant section (moment direction {angle:g}{_DEGREE})"


def plot_interaction_surface(result: InteractionSurface, *, figsize: tuple[float, float] = (7.0, 6.0), n_levels: int = 24) -> Figure:
    """3D plot of the ULS interaction surface in (M_y, M_z, N).

    The surface is resampled onto a common axial grid — each level a fixed-N ring interpolated from the
    meridians — and drawn as a coloured surface, with the axial force on the vertical axis (tension
    positive).

    Parameters
    ----------
    result : InteractionSurface
        The sampled interaction surface.
    figsize : tuple[float, float]
        Figure size in inches.
    n_levels : int
        Number of axial rings sampled across the surface's axial range.

    Returns
    -------
    Figure
        The matplotlib figure with the 3D interaction surface.
    """
    meridians = result.meridians
    n_min = max(min(point.n for point in meridian.points) for meridian in meridians)
    n_max = min(max(point.n for point in meridian.points) for meridian in meridians)
    rings = [result.ring(float(n)).points for n in np.linspace(n_min, n_max, n_levels)]
    m_y = np.array([[point.m_y for point in ring] for ring in rings])
    m_z = np.array([[point.m_z for point in ring] for ring in rings])
    axial = np.array([[point.n for point in ring] for ring in rings])

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(m_y, m_z, axial, cmap="viridis", alpha=0.85, linewidth=0.2, edgecolor="grey")
    ax.set_xlabel("$M_{y,Rd}$ [kNm]")
    ax.set_ylabel("$M_{z,Rd}$ [kNm]")
    ax.set_zlabel("$N_{Rd}$ [kN]  (tension +)")
    ax.invert_zaxis()  # compression (negative) on top, tension (positive) below
    ax.set_title("ULS interaction surface")
    fig.tight_layout()
    return fig


def plot_interaction_section(result: InteractionSection, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
    """Plot a closed planar N-M section (signed M on the x-axis, N on the y-axis, tension +).

    The plotted moment and the labels follow the section's cut kind: the signed resultant projected onto
    the moment direction for a resultant section, the signed M_y or M_z for a fixed-component section.

    Parameters
    ----------
    result : InteractionSection
        The closed N-M section.
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the closed section.
    """
    xlabel, title = _section_labels(result)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(result.signed_moments(), [point.n for point in result.points], "-o", ms=3, color=_STRESS_COLOUR)
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("$N_{Rd}$ [kN]  (tension +)")
    ax.set_title(title)
    ax.invert_yaxis()  # compression (negative) on top, tension (positive) below
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_verification(result: VerificationDiagram, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
    """Plot a capacity section with the design-action and capacity markers and the unity check.

    The closed capacity section is drawn along the design moment direction; the design action and the
    capacity are marked at the design axial force (both on the ``N = N_Ed`` line), and the title states
    the utilization. The capacity marker comes from the exact check, so it may sit marginally off the
    interpolated loop.

    Parameters
    ----------
    result : VerificationDiagram
        The verification diagram (capacity section plus unity-check result).
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the capacity section and the unity-check markers.
    """
    section = result.section
    check = result.utilization
    assert check.m_rd is not None  # a verification diagram is only built for a bending check
    n_ed = check.forces.n
    xlabel, _ = _section_labels(section)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(section.signed_moments(), [point.n for point in section.points], "-", color=_STRESS_COLOUR, lw=1.6)
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.plot([check.m_ed, check.m_rd], [n_ed, n_ed], "--", color="grey", lw=0.9)
    ax.plot(check.m_ed, n_ed, "x", color=_NEUTRAL_AXIS_COLOUR, ms=11, mew=2.2, label=f"$M_{{Ed}}$ = {check.m_ed:.1f} kNm")
    ax.plot(check.m_rd, n_ed, "x", color=_STRESS_COLOUR, ms=11, mew=2.2, label=f"$M_{{Rd}}$ = {check.m_rd:.1f} kNm")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("$N_{Rd}$ [kN]  (tension +)")
    status = "OK" if check.is_ok else "exceeded"
    ax.set_title(f"ULS verification - unity check {check.utilization:.2f} ({status})")
    ax.invert_yaxis()  # compression (negative) on top, tension (positive) below
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_biaxial_diagram(result: BiaxialInteractionResult, *, figsize: tuple[float, float] = (6.0, 6.0)) -> Figure:
    """Plot a biaxial M_y-M_z interaction envelope at a fixed axial force.

    Parameters
    ----------
    result : BiaxialInteractionResult
        The biaxial envelope result.
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the biaxial envelope.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([point.m_y for point in result.points], [point.m_z for point in result.points], "-o", ms=3, color=_STRESS_COLOUR)
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.set_xlabel("$M_{y,Rd}$ [kNm]")
    ax.set_ylabel("$M_{z,Rd}$ [kNm]")
    ax.set_title(f"Biaxial interaction envelope (N = {result.n:g} kN)")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def plot_moment_curvature(result: MomentCurvatureResult, *, figsize: tuple[float, float] = (7.0, 5.0)) -> Figure:
    """Plot a moment-curvature curve with the ultimate point marked.

    Parameters
    ----------
    result : MomentCurvatureResult
        The moment-curvature result.
    figsize : tuple[float, float]
        Figure size in inches.

    Returns
    -------
    Figure
        The matplotlib figure with the moment-curvature curve.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(result.kappa, result.m, "-", color=_STRESS_COLOUR)
    peak_index = int(np.argmax(np.asarray(result.m)))
    ax.plot(result.kappa[peak_index], result.m[peak_index], "o", color=_NEUTRAL_AXIS_COLOUR, label=f"$M_u$ = {result.m_ultimate:.1f} kNm")
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.set_xlabel(f"{_KAPPA} [1/mm]")
    ax.set_ylabel("M [kNm]")
    ax.set_title(f"Moment-curvature (N = {result.n:g} kN, {_THETA} = {result.theta:g}{_DEGREE})")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def _draw_section(
    ax: Axes,
    across: np.ndarray,
    heights: np.ndarray,
    strain: np.ndarray,
    hs: np.ndarray,
    result: StressStrainResult,
    across_axis: np.ndarray,
    height_axis: np.ndarray,
) -> None:
    """Draw the section outline, the hatched compression zone and the reinforcement (projected frame)."""
    ax.fill(across, heights, facecolor=_CONCRETE_FACE, edgecolor="black", lw=1.2)
    _shade_compression_zone(ax, across, heights, strain, hs)
    for rebar in result.rebar_results:
        point = np.array([rebar.x, rebar.y])
        ax.plot(point @ across_axis, point @ height_axis, "o", color=_REBAR_COLOUR, ms=7)
    ax.set_title("section")
    ax.set_xlabel("across neutral axis [mm]")
    ax.set_ylabel("height along strain gradient [mm]")
    ax.set_aspect("equal")


def _shade_compression_zone(ax: Axes, across: np.ndarray, heights: np.ndarray, strain: np.ndarray, hs: np.ndarray) -> None:
    """Hatch the part of the section in compression (strain < 0), clipped to the section outline.

    The concrete carries compression where the strain is negative. Since strain is linear over the
    height, that is a band bounded by the neutral axis; a hatched copy of the section outline is clipped
    to that band. A fully tensioned section shows no hatch; a fully compressed one is hatched whole.
    """
    if strain[0] >= 0 and strain[-1] >= 0:
        return  # entire section in tension: nothing compressed
    hatch = MplPolygon(np.column_stack([across, heights]), closed=True, facecolor="none", edgecolor=_COMPRESSION_HATCH, hatch="//", lw=0.0)
    ax.add_patch(hatch)
    if strain[0] < 0 and strain[-1] < 0:
        return  # entire section in compression: hatch the whole outline, no clipping needed
    neutral_height = _neutral_axis_height(strain, hs)
    if neutral_height is None:
        return  # a zero-strain end fibre; leave the full hatch
    low, high = float(heights.min()), float(heights.max())
    left, right = float(across.min()), float(across.max())
    y0, y1 = (low, neutral_height) if strain[0] < 0 else (neutral_height, high)
    hatch.set_clip_path(Rectangle((left, y0), right - left, y1 - y0, transform=ax.transData))


def _draw_strain(ax: Axes, strain: np.ndarray, hs: np.ndarray, result: StressStrainResult, height_axis: np.ndarray) -> None:
    """Draw the linear strain profile and the reinforcement strains."""
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.plot(strain, hs, color=_STRAIN_COLOUR, lw=1.8)
    ax.fill_betweenx(hs, 0.0, strain, color=_STRAIN_COLOUR, alpha=0.15)
    for value, height in ((strain[0], hs[0]), (strain[-1], hs[-1])):
        ax.annotate(f"{value:.2f}", (value, height), textcoords="offset points", xytext=(4, -4 if height == hs[-1] else 4), fontsize=8)
    for rebar in result.rebar_results:
        height = np.array([rebar.x, rebar.y]) @ height_axis
        ax.plot(rebar.strain, height, "s", color=_REBAR_COLOUR, ms=5)
        ax.annotate(f"{rebar.strain:.2f}", (rebar.strain, height), textcoords="offset points", xytext=(4, 4), color=_REBAR_COLOUR, fontsize=8)
    ax.set_title(f"{_EPSILON} [{_PER_MILLE}]")
    ax.set_xlabel(f"strain [{_PER_MILLE}]  (compression -)")


def _draw_stress(ax: Axes, stress: np.ndarray, hs: np.ndarray, result: StressStrainResult, height_axis: np.ndarray) -> None:
    """Draw the concrete stress block and, on a twin axis, the reinforcement stresses.

    Concrete (tens of MPa) and steel (hundreds of MPa) live on separate x-axes so the concrete stress
    block stays legible; both axes are set symmetric about zero so their zero-stress lines coincide.
    """
    ax.axvline(0.0, color="grey", lw=0.8)
    ax.plot(stress, hs, color=_STRESS_COLOUR, lw=1.8)
    ax.fill_betweenx(hs, 0.0, stress, color=_STRESS_COLOUR, alpha=0.2, hatch="///", edgecolor=_STRESS_COLOUR)
    extreme_index = int(np.argmax(np.abs(stress)))
    ax.annotate(f"{stress[extreme_index]:.2f}", (stress[extreme_index], hs[extreme_index]), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_xlim(_symmetric_limits(stress))
    ax.set_title(f"{_SIGMA} [MPa]")
    ax.set_xlabel("concrete stress [MPa]  (compression -)", color=_STRESS_COLOUR)
    ax.tick_params(axis="x", colors=_STRESS_COLOUR)

    if not result.rebar_results:
        return
    ax_steel = ax.twiny()
    for rebar in result.rebar_results:
        height = np.array([rebar.x, rebar.y]) @ height_axis
        ax_steel.plot([0.0, rebar.stress], [height, height], color=_REBAR_COLOUR, lw=3)
        ax_steel.annotate(f"{rebar.stress:.1f}", (rebar.stress, height), textcoords="offset points", xytext=(4, 4), color=_REBAR_COLOUR, fontsize=8)
    ax_steel.set_xlim(_symmetric_limits(np.array([rebar.stress for rebar in result.rebar_results])))
    ax_steel.set_xlabel("rebar stress [MPa]", color=_REBAR_COLOUR)
    ax_steel.tick_params(axis="x", colors=_REBAR_COLOUR)


def _symmetric_limits(values: np.ndarray, margin: float = 1.1) -> tuple[float, float]:
    """Return x-limits symmetric about zero that enclose ``values`` (so a zero line is centred)."""
    extreme = float(np.max(np.abs(values))) or 1.0
    return -margin * extreme, margin * extreme


def _neutral_axis_height(strain: np.ndarray, hs: np.ndarray) -> float | None:
    """Interpolate the height where the strain crosses zero, or ``None`` when it never changes sign."""
    if strain[0] * strain[-1] >= 0:
        return None
    return float(np.interp(0.0, strain, hs) if strain[-1] > strain[0] else np.interp(0.0, strain[::-1], hs[::-1]))


def _draw_neutral_axis(axes: tuple[Axes, ...] | list[Axes], strain: np.ndarray, hs: np.ndarray) -> None:
    """Draw the neutral (zero-strain) line across all panels when it lies within the section."""
    h_na = _neutral_axis_height(strain, hs)
    if h_na is None:
        return  # no sign change -> no neutral axis inside the section
    for ax in axes:
        ax.axhline(h_na, color=_NEUTRAL_AXIS_COLOUR, ls="--", lw=1.0)
