"""RHSCF Corner cross-section."""

import math
from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM, MM2


@dataclass(frozen=True)
class RHSCFCornerCrossSection(CrossSection):
    """
    Rectangular Hollow Section (RHSCF) corner cross-section.

    Parameters
    ----------
    thickness_vertical : MM
        Thickness of the vertical section
    thickness_horizontal : MM
        Thickness of the horizontal section
    inner_radius : MM
        Inner radius of the corner
    outer_radius : MM
        Outer radius of the corner
    x : MM
        x-coordinate of the lower-left corner (default 0)
    y : MM
        y-coordinate of the lower-left corner (default 0)
    name : str
        Name of the cross-section (default "RHSCF Corner")
    """

    thickness_vertical: MM
    thickness_horizontal: MM
    inner_radius: MM
    outer_radius: MM
    x: MM = 0
    y: MM = 0
    name: str = "RHSCF Corner"

    def __post_init__(self) -> None:
        """Validate input parameters after initialization."""
        if self.thickness_vertical <= 0:
            raise ValueError(f"Thickness vertical must be positive, got {self.thickness_vertical}")
        if self.thickness_horizontal <= 0:
            raise ValueError(f"Thickness horizontal must be positive, got {self.thickness_horizontal}")
        if self.inner_radius <= 0:
            raise ValueError(f"Inner radius must be positive, got {self.inner_radius}")
        if self.outer_radius <= 0:
            raise ValueError(f"Outer radius must be positive, got {self.outer_radius}")

    @property
    def width_rectangle(self) -> MM:
        """Width of the rectangle part of the RHSCF corner cross-section [mm]."""
        return self.thickness_vertical + self.inner_radius

    @property
    def height_rectangle(self) -> MM:
        """Height of the rectangle part of the RHSCF corner cross-section [mm]."""
        return self.thickness_horizontal + self.inner_radius

    @property
    def polygon(self) -> Polygon:
        """
        Shapely Polygon representing the RHSCF corner cross-section.
        """

        ll = (self.x + self.inner_radius, self.y)
        lr = (self.x + self.width_rectangle, self.y)
        ur = (self.x + self.width_rectangle, self.y + self.height_rectangle - self.outer_radius)
        ul = (self.x, self.y + self.height_rectangle)

        n = 32

        # Outer arc (from vertical to horizontal)
        outer_arc = [
            (
                self.x + self.width_rectangle - self.outer_radius + self.outer_radius * math.cos(math.radians(0 + i * 90 / (n - 1))),
                self.y + self.height_rectangle - self.outer_radius + self.outer_radius * math.sin(math.radians(0 + i * 90 / (n - 1))),
            )
            for i in range(n)
        ]
        
        # Inner arc (from horizontal to vertical, reversed)
        inner_arc = [
            (
                self.x + self.inner_radius * math.cos(math.radians(0 + i * 90 / (n - 1))),
                self.y + self.inner_radius * math.sin(math.radians(0 + i * 90 / (n - 1))),
            )
            for i in range(n)
        ][::-1]

        points = [lr, *outer_arc, ul, *inner_arc]
        return Polygon(points)

    @property
    def area(self) -> MM2:
        """Area of the RHSCF corner cross-section [mm²]."""
        area_rectangle = self.width_rectangle * self.height_rectangle
        area_inner_circle = math.pi * (self.inner_radius**2) / 4
        area_outer_circle_spandrel = self.outer_radius**2 - math.pi * (self.outer_radius**2) / 4
        return area_rectangle - area_inner_circle - area_outer_circle_spandrel

    def geometry(self, mesh_size: MM | None = None) -> Geometry:
        """
        Return the geometry of the RHSCF corner cross-section.

        Parameters
        ----------
        mesh_size : MM | None
            Maximum mesh element area to be used within the Geometry-object finite-element mesh. If not provided, a default value will be used.
        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(min(self.thickness_vertical, self.thickness_horizontal) / 20, minimum_mesh_size)
            mesh_size = mesh_length**2

        geom = Geometry(geom=self.polygon)
        geom.create_mesh(mesh_sizes=mesh_size)
        return geom

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Example parameters
    thickness_vertical = 10
    thickness_horizontal = 10
    inner_radius = 10
    outer_radius = 10
    x = 0
    y = 0

    section = RHSCFCornerCrossSection(
        thickness_vertical=thickness_vertical,
        thickness_horizontal=thickness_horizontal,
        inner_radius=inner_radius,
        outer_radius=outer_radius,
        x=x,
        y=y,
    )

    poly = section.polygon

    fig, ax = plt.subplots()
    x, y = poly.exterior.xy
    ax.plot(x, y, label="RHSCF Corner")
    ax.set_aspect("equal")
    ax.set_title("RHSCF Corner Cross-Section Example")
    ax.legend()
    plt.show()