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

from blueprints.structural_sections.concrete.reinforced_concrete_sections.plotters.rectangular import RCS_CROSS_SECTION_COLOR, REBAR_COLOR
from blueprints.type_alias import MPA
from blueprints.unit_conversion import PER_MILLE_TO_RATIO

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import StrainPlane, StressStrainResult

# Strain gradient (ratio/mm) below which the section is treated as having no neutral axis (pure axial).
_CURVATURE_TOL: float = 1e-12
_N_SAMPLES: int = 100

# Concrete and reinforcement in the same colours as the cross-section plotters.
_CONCRETE_FACE = RCS_CROSS_SECTION_COLOR
_REBAR_COLOUR = REBAR_COLOR
_STRAIN_COLOUR = "tab:blue"
_STRESS_COLOUR = "tab:red"
_NEUTRAL_AXIS_COLOUR = "green"
_COMPRESSION_HATCH = "grey"
_DIMENSION_COLOUR = "black"

# Width ratios of the section, strain and stress panels; the section ratio is then fitted to the section's shape.
_PANEL_WIDTH_RATIOS: tuple[float, float, float] = (1.0, 1.3, 1.3)
# Layout passes used to fit the section panel to the full height of the strain and stress panels, and the largest
# share of the figure width the section panel may take (a very wide section keeps the other panels readable).
_LAYOUT_PASSES: int = 6
_MAX_SECTION_SHARE: float = 0.4
# Matplotlib's default horizontal data margin, as a fraction of the section width on either side.
_X_MARGIN: float = 0.05
# Gap between the section and the compression-depth dimension line, and the room for its label to the right of
# that line, as fractions of the section width.
_DIMENSION_OFFSET: float = 0.12
_DIMENSION_LABEL_ROOM: float = 0.25
# Neutral-axis angles (deg) within this tolerance of 0 or -90 count as bending about a single axis.
_UNIAXIAL_ANGLE_TOL: float = 1e-6

# Axis-label symbols kept as chr() so the source stays ASCII (avoids ambiguous-unicode lint in string literals).
_EPSILON = chr(0x03B5)  # ε
_SIGMA = chr(0x03C3)  # σ
_PER_MILLE = chr(0x2030)  # ‰


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


def _concrete_stress(strain_per_mille: np.ndarray, elastic_modulus: MPA, *, is_cracked: bool) -> np.ndarray:
    """Concrete stress from strain following the linear SLS law.

    Parameters
    ----------
    strain_per_mille : np.ndarray
        Strain samples [‰], compression negative.
    elastic_modulus : MPA
        The concrete elastic modulus (e_cm or E_c,eff) [MPa].
    is_cracked : bool
        Whether the concrete tension stress must be dropped (cracked SLS regime).

    Returns
    -------
    np.ndarray
        Concrete stress samples [MPa], compression negative.
    """
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
    stress = _concrete_stress(strain, result.elastic_modulus, is_cracked=result.is_cracked)

    fig, (ax_section, ax_strain, ax_stress) = plt.subplots(
        1, 3, figsize=figsize, sharey=True, gridspec_kw={"width_ratios": list(_PANEL_WIDTH_RATIOS)}
    )

    _draw_section(ax_section, across, heights, strain, hs, result, across_axis, height_axis)
    if _shows_compression_depth(plane, strain, hs):
        _draw_compression_depth(ax_section, plane, across, strain, hs)
    _draw_strain(ax_strain, strain, hs, result, height_axis)
    _draw_stress(ax_stress, stress, hs, result, height_axis)
    _draw_neutral_axis((ax_section, ax_strain, ax_stress), strain, hs)

    regime = {"SLS_UNCRACKED": "uncracked", "SLS_CRACKED": "cracked"}[result.regime.value]
    fig.suptitle(f"Strain & stress over height - {regime}", fontsize=11)
    fig.tight_layout()
    _fit_section_panel_height(fig, ax_section, ax_strain)
    return fig


def _fit_section_panel_height(fig: Figure, ax_section: Axes, ax_reference: Axes) -> None:
    """Widen or narrow the section panel until it has the full height of the strain and stress panels.

    The section is drawn to scale, so its panel shrinks in height when its shape is wider than the panel. The
    panels share the height axis, so a shorter section panel would put the neutral axis at a different height
    than in the other panels. The section panel's share of the figure width is scaled by the missing height. A
    section too wide for that (a slab, or a beam bent about its vertical axis) keeps its reduced height, and the
    other panels are shortened to match it instead.
    """
    gridspec = ax_section.get_gridspec()
    assert gridspec is not None  # created by plt.subplots
    others = sum(_PANEL_WIDTH_RATIOS[1:])
    section_ratio = _PANEL_WIDTH_RATIOS[0]
    for _ in range(_LAYOUT_PASSES):
        ax_section.apply_aspect()
        missing = ax_reference.get_position().height / ax_section.get_position().height
        if math.isclose(missing, 1.0, rel_tol=1e-3):
            return
        share = min(section_ratio / (section_ratio + others) * missing, _MAX_SECTION_SHARE)
        section_ratio = others * share / (1.0 - share)
        gridspec.set_width_ratios([section_ratio, *_PANEL_WIDTH_RATIOS[1:]])
        fig.tight_layout()
    ax_section.apply_aspect()
    section = ax_section.get_position()
    for ax in fig.axes:
        if ax is not ax_section:
            position = ax.get_position()
            ax.set_position((position.x0, section.y0, position.width, section.height))


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


def _shows_compression_depth(plane: StrainPlane, strain: np.ndarray, hs: np.ndarray) -> bool:
    """Whether the compression-zone depth is dimensioned: bending about a single axis, neutral axis inside the section.

    Under biaxial bending the depth is not a single section height, so it is left out.
    """
    uniaxial = any(math.isclose(plane.neutral_axis_angle, angle, abs_tol=_UNIAXIAL_ANGLE_TOL) for angle in (0.0, -90.0))
    return uniaxial and plane.neutral_axis_depth is not None and _neutral_axis_height(strain, hs) is not None


def _draw_compression_depth(ax: Axes, plane: StrainPlane, across: np.ndarray, strain: np.ndarray, hs: np.ndarray) -> None:
    """Dimension the depth of the compression zone beside the section.

    The dimension runs from the extreme compression fibre to the neutral axis and is labelled with the
    actual neutral-axis depth of the strain plane. Only called when :func:`_shows_compression_depth` holds.
    """
    h_na = _neutral_axis_height(strain, hs)
    assert h_na is not None  # guaranteed by _shows_compression_depth
    h_compression = float(hs[0] if strain[0] < strain[-1] else hs[-1])  # extreme compression fibre
    left, right = float(across.min()), float(across.max())
    x_dim = right + _DIMENSION_OFFSET * (right - left)
    ax.annotate("", xy=(x_dim, h_compression), xytext=(x_dim, h_na), arrowprops={"arrowstyle": "<->", "color": _DIMENSION_COLOUR, "lw": 1.0})
    ax.text(
        x_dim + 0.04 * (right - left),
        (h_compression + h_na) / 2,
        f"x = {plane.neutral_axis_depth:.1f} mm",
        rotation=90,
        ha="left",
        va="center",
        fontsize=8.5,
        color=_DIMENSION_COLOUR,
    )
    ax.set_xlim(left - _X_MARGIN * (right - left), x_dim + _DIMENSION_LABEL_ROOM * (right - left))


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
