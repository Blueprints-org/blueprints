"""Defines a general steel plotter for cross sections and its characteristics."""

import matplotlib.pyplot as plt
from matplotlib import patches as mplpatches
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Point

from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection

# Define color
STEEL_COLOR = (0.683, 0.0, 0.0)


def plot_shapes(
    profile: CombinedSteelCrossSection,
    figsize: tuple[float, float] = (15.0, 8.0),
    title: str = "",
    font_size_title: float = 18.0,
    font_size_legend: float = 10.0,
    show: bool = False,
) -> plt.Figure:
    """
    Plot the given shapes.

    Parameters
    ----------
    profile : SteelCrossSection
        The steel cross-sections to plot.
    figsize : tuple[float, float], optional
        The size of the figure in inches. Default is (15.0, 8.0).
    title : str, optional
        The title of the plot. Default is "".
    font_size_title : float, optional
        The font size of the title. Default is 18.0.
    font_size_legend : float, optional
        The font size of the legend. Default is 10.0.
    show : bool, optional
        Whether to show the plot. Default is False.
    """
    fig, ax = plt.subplots(figsize=figsize)

    for element in profile.elements:
        # Plot the exterior polygon
        x, y = element.cross_section.polygon.exterior.xy
        patch = MplPolygon(xy=list(zip(x, y)), lw=1, fill=True, facecolor=STEEL_COLOR, edgecolor=STEEL_COLOR)
        ax.add_patch(patch)

        # Plot the interior polygons (holes) if any
        for interior in element.cross_section.polygon.interiors:
            x, y = interior.xy
            patch = MplPolygon(xy=list(zip(x, y)), lw=0, fill=True, facecolor="white")
            ax.add_patch(patch)

    # Add dimension lines and centroid
    _add_dimension_lines(ax=ax, profile=profile, centroid=profile.centroid)
    ax.plot(profile.centroid.x, profile.centroid.y, "o", color="black")

    # Add legend text
    profile_section_properties = profile.section_properties(plastic=False, warping=False)
    legend_text = f"""
    {profile.name}\n
    Area: {profile.area:.1f} mm²
    Weight per meter: {profile.weight_per_meter:.1f} kg/m
    Moment of inertia about x: {profile_section_properties.ixx_c:.0f} mm⁴
    Moment of inertia about y: {profile_section_properties.iyy_c:.0f} mm⁴
    """

    # Add the steel quality if all elements have the same material
    if len({element.material.name for element in profile.elements}) == 1:
        legend_text += f"Steel quality: {profile.elements[0].material.name}\n"

    # Get the boundaries of the plot
    _, min_y, max_x, _ = profile.polygon.bounds
    offset = profile.width / 20

    # Add the legend text to the plot
    ax.annotate(
        xy=(max_x + offset, min_y),
        text=legend_text,
        transform=ax.transAxes,
        fontsize=font_size_legend,
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(title, fontsize=font_size_title)
    ax.grid(True)
    ax.axis("equal")
    ax.axis("off")
    ax.set_xlim(profile.polygon.bounds[0] - offset, profile.polygon.bounds[2] + offset)

    if show:
        plt.show()  # pragma: no cover

    assert fig is not None

    return fig


def _add_dimension_lines(ax: plt.Axes, profile: CombinedSteelCrossSection, centroid: Point) -> None:
    """Adds dimension lines to show the outer dimensions of the geometry.

    Parameters
    ----------
    ax : plt.Axes
        The matplotlib axes to draw on.
    profile : tuple[CrossSection, ...]
        The cross-sections to plot.
    centroid : Point
        The centroid of the cross-section.
    """
    # Define the offset for the dimension lines
    offset_dimension_lines = max(profile.height, profile.width) / 20
    offset_text = offset_dimension_lines / 2

    # Calculate the bounds of all elements in the geometry
    min_x, min_y, max_x, max_y = profile.polygon.bounds

    # Calculate the width and height of the geometry relative to the centroid
    centroid_width = centroid.x - min_x
    centroid_height = centroid.y - min_y

    # Add the width dimension line (below the geometry)
    diameter_line_style = {
        "arrowstyle": mplpatches.ArrowStyle(stylename="<->", head_length=0.5, head_width=0.5),
    }

    # HORIZONTAL DIMENSION LINES (BELOW THE GEOMETRY)
    # Add the width dimension lines (below the geometry)
    ax.annotate(
        text="",
        xy=(min_x, min_y - offset_dimension_lines * 2),
        xytext=(max_x, min_y - offset_dimension_lines * 2),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        annotation_clip=False,
    )
    ax.text(
        s=f"b= {profile.width:.1f} mm",
        x=(min_x + max_x) / 2,
        y=min_y - offset_dimension_lines * 2 + offset_text,
        verticalalignment="top",
        horizontalalignment="center",
        fontsize=10,
    )

    # Add the width dimension lines (below the geometry)
    ax.annotate(
        text="",
        xy=(min_x, min_y - offset_dimension_lines),
        xytext=(centroid.x, min_y - offset_dimension_lines),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        annotation_clip=False,
    )
    ax.text(
        s=f"{centroid_width:.1f} mm",
        x=(min_x + centroid.x) / 2,
        y=min_y - offset_dimension_lines + offset_text,
        verticalalignment="top",
        horizontalalignment="center",
        fontsize=10,
    )

    # HEIGHT DIMENSION LINES (ON THE LEFT SIDE OF THE GEOMETRY)
    # Add the distance from the bottom to the centroid (on the left side)
    ax.annotate(
        text="",
        xy=(min_x - offset_dimension_lines, min_y),
        xytext=(min_x - offset_dimension_lines, centroid.y),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        rotation=90,
        annotation_clip=False,
    )
    ax.text(
        s=f"{centroid_height:.1f} mm",
        x=min_x - offset_dimension_lines - offset_text,
        y=(min_y + centroid.y) / 2,
        verticalalignment="center",
        horizontalalignment="left",
        fontsize=10,
        rotation=90,
    )

    # # Add the height dimension line (on the left side of the geometry)
    ax.annotate(
        text="",
        xy=(min_x - offset_dimension_lines * 2, max_y),
        xytext=(min_x - offset_dimension_lines * 2, min_y),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        rotation=90,
        annotation_clip=False,
    )
    ax.text(
        s=f"h= {profile.height:.1f} mm",
        x=(min_x - offset_dimension_lines * 2 - offset_text),
        y=(min_y + max_y) / 2,
        verticalalignment="center",
        horizontalalignment="left",
        fontsize=10,
        rotation=90,
    )
