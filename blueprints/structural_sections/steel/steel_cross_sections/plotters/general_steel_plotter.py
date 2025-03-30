"""Defines a general steel plotter for cross sections and its characteristics."""
# ruff: noqa: PLR0913, F821

import matplotlib.pyplot as plt
from matplotlib import patches as mplpatches
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Point, Polygon

from blueprints.materials.steel import SteelStrengthClass
from blueprints.structural_sections.general_cross_section import CrossSection

# Define color
STEEL_COLOR = (0.683, 0.0, 0.0)


def plot_shapes(
    *elements: CrossSection,
    centroid: Point,
    figsize: tuple[float, float] = (15.0, 8.0),
    title: str = "Cross Section",
    font_size_title: float = 18.0,
    font_size_legend: float = 10.0,
    show: bool = False,
) -> plt.Figure:
    """
    Plot the given shapes.

    Parameters
    ----------
    elements : CrossSection
        The cross-sections to plot.
    centroid : Point
        The centroid of the cross-section.
    figsize : tuple[float, float], optional
        The size of the figure in inches. Default is (15.0, 8.0).
    title : str, optional
        The title of the plot. Default is "Cross Section".
    font_size_title : float, optional
        The font size of the title. Default is 18.0.
    font_size_legend : float, optional
        The font size of the legend. Default is 10.0.
    show : bool, optional
        Whether to show the plot. Default is False.
    """
    fig, ax = plt.subplots(figsize=figsize)

    legend_text = ""

    for element in elements:
        if not isinstance(element.geometry, Polygon):
            raise TypeError(f"All shapes must be Shapely polygons, but got: {type(element.geometry)}")

        # Plot the exterior polygon
        x, y = element.geometry.exterior.xy
        patch = MplPolygon(xy=list(zip(x, y)), lw=1, fill=True, facecolor=STEEL_COLOR, edgecolor=STEEL_COLOR)
        ax.add_patch(patch)

        # Plot the interior polygons (holes) if any
        for interior in element.geometry.interiors:
            x, y = interior.xy
            patch = MplPolygon(xy=list(zip(x, y)), lw=0, fill=True, facecolor="white")
            ax.add_patch(patch)

        # Add element details to the legend
        legend_text += f"{element.name}:\n"
        attributes = {
            "plate_thickness": "Thickness",
            "radius": "Radius",
            "radius_centerline": "Center Radius",
            "side_length": "Side Length",
            "outer_diameter": "Outer Diameter",
        }

        for attr, label in attributes.items():
            if hasattr(element, attr):
                legend_text += f"  {label}={getattr(element, attr):.1f} mm\n"
        legend_text += f"  Area={element.area:.1f} mm²\n\n"
    legend_text = legend_text[:-4]

    # Add dimension lines
    _add_dimension_lines(ax, elements, centroid)

    # Plot the centroid
    if centroid:
        ax.plot(centroid.x, centroid.y, "o", color="black")

    # Add legend text
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
        plt.show()

    assert fig is not None
    return fig


def _add_dimension_lines(ax: plt.Axes, elements: tuple[CrossSection, ...], centroid: Point) -> None:
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
        bounds = element.geometry.bounds
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


# Example usage
if __name__ == "__main__":
    from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile

    # Define a sample CHS profile
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = CHSSteelProfile(outer_diameter=1000, wall_thickness=10, steel_class=steel_class)
    profile.plot(show=True)
