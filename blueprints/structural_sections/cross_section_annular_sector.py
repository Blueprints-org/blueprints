"""Annular sector cross-section shape."""

import math
from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely.affinity import rotate
from shapely.geometry import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import DEG, MM


@dataclass(frozen=True)
class AnnularSectorCrossSection(CrossSection):
    """
    Class to represent an annular sector cross-section using shapely for geometric calculations.

    Parameters
    ----------
    inner_radius : MM
        The radius of the inner circle of the annular sector [mm].
    thickness : MM
        The thickness of the annular sector cross-section [mm].
    start_angle : DEG
        The start angle of the annular sector in degrees (top = 0 degrees, clockwise is positive).
    end_angle : DEG
        The end angle of the annular sector in degrees (must be larger than start angle but not more than 360 degrees more).
    x : MM
        The x-coordinate of the annular sector's radius center.
    y : MM
        The y-coordinate of the annular sector's radius center.
    name : str
        The name of the rectangular cross-section, default is "Annular Sector".
    """

    inner_radius: MM
    thickness: MM
    start_angle: DEG
    end_angle: DEG
    x: MM
    y: MM
    name: str = "Annular Sector"

    def __post_init__(self) -> None:
        """Post-initialization to validate the inputs."""
        if self.inner_radius < 0:
            raise ValueError(f"Radius must be zero or positive, but got {self.inner_radius}")
        if self.thickness <= 0:
            raise ValueError(f"Thickness must be a positive value, but got {self.thickness}")
        if self.start_angle > 360 or self.start_angle < -360:
            raise ValueError(f"Start angle must be between -360 and 360 degrees, but got {self.start_angle}")
        if self.end_angle <= self.start_angle:
            raise ValueError(f"End angle must be greater than start angle, but got end angle {self.end_angle} and start angle {self.start_angle}")
        if self.end_angle - self.start_angle >= 360:
            raise ValueError(
                f"The total angle made between start and end angle must be less than 360 degrees, but got "
                f"{self.end_angle - self.start_angle} degrees (end {self.end_angle} - start {self.start_angle})\n\n"
                f"In case you want to create a full circle (donut shape), "
                "use a tube cross section instead (TubeCrossSection)."
            )

    @property
    def radius_centerline(self) -> MM:
        """Calculate the inner radius of the annular sector [mm]."""
        return self.inner_radius + self.thickness / 2.0

    @property
    def outer_radius(self) -> MM:
        """Calculate the outer radius of the annular sector [mm]."""
        return self.radius_centerline + self.thickness / 2.0

    @property
    def height(self) -> MM:
        """
        Calculate the height of the annular sector cross-section [mm].

        Returns
        -------
        MM
            The height of the annular sector.
        """
        min_y = min(y for _, y in self.polygon.exterior.coords)
        max_y = max(y for _, y in self.polygon.exterior.coords)
        return max_y - min_y

    @property
    def width(self) -> MM:
        """
        Calculate the width of the annular sector cross-section [mm].

        Returns
        -------
        MM
            The width of the annular sector.
        """
        min_x = min(x for x, _ in self.polygon.exterior.coords)
        max_x = max(x for x, _ in self.polygon.exterior.coords)
        return max_x - min_x

    @property
    def polygon(self) -> Polygon:
        """
        Shapely Polygon representing the annular sector cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the annular sector.
        """
        center = Point(self.x, self.y)
        inner_circle = center.buffer(self.inner_radius, quad_segs=64)
        outer_circle = center.buffer(self.outer_radius, quad_segs=64)

        inner_ring = rotate(inner_circle, -self.start_angle, origin=center)
        outer_ring = rotate(outer_circle, -self.start_angle, origin=center)

        # Create the annular sector by intersecting with a sector
        sector_points = [center]
        angle_step = (self.end_angle - self.start_angle) / 8
        for i in range(9):
            angle = math.radians(90 - self.start_angle - i * angle_step)
            sector_points.append(Point(center.x + 2 * self.outer_radius * math.cos(angle), center.y + 2 * self.outer_radius * math.sin(angle)))
        sector_points.append(center)
        sector = Polygon(sector_points).buffer(0)

        result = outer_ring.difference(inner_ring).intersection(sector)
        return Polygon(result)  # type: ignore[arg-type]

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the annular sector cross-section.

        Parameters
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        Returns
        -------
        Geometry
            The Geometry object representing the annular sector.
        """
        if mesh_size is None:
            minimum_mesh_size = 1.0
            mesh_length = max(self.thickness / 5, minimum_mesh_size)
            mesh_size = mesh_length**2

        annular_sector = Geometry(geom=self.polygon)
        annular_sector.create_mesh(mesh_sizes=mesh_size)
        return annular_sector
