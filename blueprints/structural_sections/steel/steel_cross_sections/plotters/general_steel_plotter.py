"""Defines a general steel plotter for cross sections and its characteristics."""
# ruff: noqa: PLR0913, F821

import matplotlib.pyplot as plt
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
    show : bool, optional
        Whether to show the plot. Default is False.
    """
    fig, ax = plt.subplots(figsize=figsize)

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

    # Plot the centroid
    if centroid:
        ax.plot(centroid.x, centroid.y, "o", color="black")

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


# Example usage
if __name__ == "__main__":
    from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile

    # Define a sample CHS profile
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = CHSSteelProfile(outer_diameter=100, wall_thickness=10, steel_class=steel_class)
    profile.plot(show=True)
