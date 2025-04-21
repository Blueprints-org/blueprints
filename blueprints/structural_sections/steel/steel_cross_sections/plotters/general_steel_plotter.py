"""Defines a general steel plotter for cross sections and its characteristics."""
# ruff: noqa: PLR0913, F821

import matplotlib.pyplot as plt
from matplotlib import patches as mplpatches
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Point

from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import SteelCrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement

# Define color
STEEL_COLOR = (0.683, 0.0, 0.0)


def plot_shapes(
    profile: SteelCrossSection,
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
        x, y = element.polygon.exterior.xy
        patch = MplPolygon(xy=list(zip(x, y)), lw=1, fill=True, facecolor=STEEL_COLOR, edgecolor=STEEL_COLOR)
        ax.add_patch(patch)

        # Plot the interior polygons (holes) if any
        for interior in element.polygon.interiors:
            x, y = interior.xy
            patch = MplPolygon(xy=list(zip(x, y)), lw=0, fill=True, facecolor="white")
            ax.add_patch(patch)

    # Add dimension lines and centroid
    _add_dimension_lines(ax, profile.elements, profile.centroid)
    ax.plot(profile.centroid.x, profile.centroid.y, "o", color="black")

    # Add legend text
    legend_text = f"Total area: {profile.steel_area:.1f} mm²\n"
    legend_text += f"Weight per meter: {profile.steel_weight_per_meter:.1f} kg/m\n"
    legend_text += f"Moment of inertia about y: {profile.moment_of_inertia_about_y:.0f} mm⁴\n"
    legend_text += f"Moment of inertia about z: {profile.moment_of_inertia_about_z:.0f} mm⁴\n"
    legend_text += f"Steel quality: {profile.steel_material.name}\n"

    ax.text(
        x=0.05,
        y=0.95,
        s=legend_text,
        transform=ax.transAxes,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=font_size_legend,
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(title, fontsize=font_size_title)
    ax.grid(True)
    ax.axis("equal")
    ax.axis("off")

    if show:
        plt.show()  # pragma: no cover

    assert fig is not None
    return fig


def _add_dimension_lines(ax: plt.Axes, elements: list[SteelElement], centroid: Point) -> None:
    """Adds dimension lines to show the outer dimensions of the geometry.

    Parameters
    ----------
    ax : plt.Axes
        The matplotlib axes to draw on.
    elements : tuple[CrossSection, ...]
        The cross-sections to plot.
    centroid : Point
        The centroid of the cross-section.
    """
    # Calculate the bounds of all elements in the geometry
    min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf")
    for element in elements:
        bounds = element.polygon.bounds
        min_x = min(min_x, bounds[0])
        min_y = min(min_y, bounds[1])
        max_x = max(max_x, bounds[2])
        max_y = max(max_y, bounds[3])

    width = max_x - min_x
    height = max_y - min_y
    centroid_width = centroid.x - min_x
    centroid_height = centroid.y - min_y

    # Add the width dimension line (below the geometry)
    diameter_line_style = {
        "arrowstyle": mplpatches.ArrowStyle(stylename="<->", head_length=0.5, head_width=0.5),
    }
    offset_width = max(height, width) / 20
    ax.annotate(
        text="",
        xy=(min_x, min_y - offset_width),
        xytext=(max_x, min_y - offset_width),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        annotation_clip=False,
    )
    ax.text(
        s=f"{width:.1f} mm",
        x=(min_x + max_x) / 2,
        y=min_y - offset_width - 1,
        verticalalignment="top",
        horizontalalignment="center",
        fontsize=10,
    )

    # Add the height dimension line (on the right side of the geometry)
    offset_height = offset_width
    ax.annotate(
        text="",
        xy=(max_x + offset_height, max_y),
        xytext=(max_x + offset_height, min_y),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        rotation=90,
        annotation_clip=False,
    )
    ax.text(
        s=f"{height:.1f} mm",
        x=max_x + offset_height + 1 + height / 200,
        y=(min_y + max_y) / 2,
        verticalalignment="center",
        horizontalalignment="left",
        fontsize=10,
        rotation=90,
    )

    # Add the distance from the left to the centroid (below the geometry, double offset)
    offset_centroid_left_bottom = 2 * offset_width
    ax.annotate(
        text="",
        xy=(min_x, min_y - offset_centroid_left_bottom),
        xytext=(centroid.x, min_y - offset_centroid_left_bottom),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        annotation_clip=False,
    )
    ax.text(
        s=f"{centroid_width:.1f} mm",
        x=(min_x + centroid.x) / 2,
        y=min_y - offset_centroid_left_bottom - 1,
        verticalalignment="top",
        horizontalalignment="center",
        fontsize=10,
    )

    # Add the distance from the bottom to the centroid (on the right side, double offset)
    offset_centroid_bottom_right = 2 * offset_height
    ax.annotate(
        text="",
        xy=(max_x + offset_centroid_bottom_right, min_y),
        xytext=(max_x + offset_centroid_bottom_right, centroid.y),
        verticalalignment="center",
        horizontalalignment="center",
        arrowprops=diameter_line_style,
        rotation=90,
        annotation_clip=False,
    )
    ax.text(
        s=f"{centroid_height:.1f} mm",
        x=max_x + offset_centroid_bottom_right + 1 + height / 200,
        y=(min_y + centroid.y) / 2,
        verticalalignment="center",
        horizontalalignment="left",
        fontsize=10,
        rotation=90,
    )
