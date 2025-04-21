"""Base class of all steel cross-sections."""

from abc import ABC

from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties
from sectionproperties.pre import Geometry
from shapely.geometry import Point, Polygon

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import KG_M, M3_M, MM, MM2
from blueprints.unit_conversion import MM3_TO_M3


class SteelCrossSection(ABC):
    """Base class of all steel cross-sections."""

    def __init__(
        self,
        steel_material: SteelMaterial,
    ) -> None:
        """Initialize the steel cross-section.

        Parameters
        ----------
        steel_material : SteelMaterial
            Material properties of the steel.
        """
        self.steel_material = steel_material  # pragma: no cover
        self.elements: list[SteelElement] = []  # pragma: no cover

    @property
    def polygon(self) -> Polygon:
        """Return the polygon of the steel cross-section."""
        combined_polygon = self.elements[0].polygon
        for element in self.elements[1:]:
            combined_polygon = combined_polygon.union(element.polygon)
        return combined_polygon

    @property
    def steel_volume_per_meter(self) -> M3_M:
        """Total volume of the reinforced cross-section per meter length [m³/m]."""
        length = 1000  # mm
        return sum(element.area * length * MM3_TO_M3 for element in self.elements)

    @property
    def steel_weight_per_meter(self) -> KG_M:
        """Total weight of the steel elements per meter length [kg/m]."""
        return self.steel_material.density * self.steel_volume_per_meter

    @property
    def area(self) -> MM2:
        """Total cross sectional area of the steel element [mm²]."""
        return sum(element.area for element in self.elements)

    @property
    def centroid(self) -> Point:
        """Centroid of the steel cross-section."""
        area_weighted_centroids_x = sum(element.centroid.x * element.area for element in self.elements)
        area_weighted_centroids_y = sum(element.centroid.y * element.area for element in self.elements)
        centroid_x = area_weighted_centroids_x / self.area
        centroid_y = area_weighted_centroids_y / self.area
        return Point(centroid_x, centroid_y)

    @property
    def moment_of_inertia_about_y(self) -> KG_M:
        """Moment of inertia about the y-axis per meter length [mm⁴]."""
        body_moments_of_inertia = sum(element.moment_of_inertia_about_y for element in self.elements)
        parallel_axis_theorem = sum(element.area * (element.centroid.y - self.centroid.y) ** 2 for element in self.elements)
        return body_moments_of_inertia + parallel_axis_theorem

    @property
    def moment_of_inertia_about_z(self) -> KG_M:
        """Moment of inertia about the z-axis per meter length [mm⁴]."""
        body_moments_of_inertia = sum(element.moment_of_inertia_about_z for element in self.elements)
        parallel_axis_theorem = sum(element.area * (element.centroid.x - self.centroid.x) ** 2 for element in self.elements)
        return body_moments_of_inertia + parallel_axis_theorem

    @property
    def elastic_section_modulus_about_y_positive(self) -> KG_M:
        """Elastic section modulus about the y-axis on the positive z side [mm³]."""
        distance_to_top = max(y for element in self.elements for _, y in element.geometry.points) - self.centroid.y
        return self.moment_of_inertia_about_y / distance_to_top

    @property
    def elastic_section_modulus_about_y_negative(self) -> KG_M:
        """Elastic section modulus about the y-axis on the negative z side [mm³]."""
        distance_to_bottom = self.centroid.y - min(y for element in self.elements for _, y in element.geometry.points)
        return self.moment_of_inertia_about_y / distance_to_bottom

    @property
    def elastic_section_modulus_about_z_positive(self) -> KG_M:
        """Elastic section modulus about the z-axis on the positive y side [mm³]."""
        distance_to_right = max(x for element in self.elements for x, _ in element.geometry.points) - self.centroid.x
        return self.moment_of_inertia_about_z / distance_to_right

    @property
    def elastic_section_modulus_about_z_negative(self) -> KG_M:
        """Elastic section modulus about the z-axis on the negative y side [mm³]."""
        distance_to_left = self.centroid.x - min(x for element in self.elements for x, _ in element.geometry.points)
        return self.moment_of_inertia_about_z / distance_to_left

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        """
        if mesh_size is None:
            mesh_size = 2.0

        geom = Geometry(geom=self.polygon)
        geom.create_mesh(mesh_sizes=mesh_size)
        return geom

    def section(self) -> Section:
        """Section object representing the cross-section."""
        return Section(geometry=self.geometry)

    def section_properties(
        self,
        geometric: bool = True,
        plastic: bool = True,
        warping: bool = True,
    ) -> SectionProperties:
        """Calculate and return the section properties of the cross-section.

        Parameters
        ----------
        geometric : bool
            Whether to calculate geometric properties.
        plastic: bool
            Whether to calculate plastic properties.
        warping: bool
            Whether to calculate warping properties.
        """
        section = self.section()

        if any([geometric, plastic, warping]):
            section.calculate_geometric_properties()
        if warping:
            section.calculate_warping_properties()
        if plastic:
            section.calculate_plastic_properties()
        return section.section_props
