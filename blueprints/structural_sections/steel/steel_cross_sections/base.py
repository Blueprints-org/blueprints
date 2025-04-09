"""Base class of all steel cross-sections."""

from abc import ABC

from shapely.geometry import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import KG_M, M3_M, MM2
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
    def steel_volume_per_meter(self) -> M3_M:
        """Total volume of the reinforced cross-section per meter length [m³/m]."""
        length = 1000  # mm
        return sum(element.area * length * MM3_TO_M3 for element in self.elements)

    @property
    def steel_weight_per_meter(self) -> KG_M:
        """Total weight of the steel elements per meter length [kg/m]."""
        return self.steel_material.density * self.steel_volume_per_meter

    @property
    def steel_area(self) -> MM2:
        """Total cross sectional area of the steel element [mm²]."""
        return sum(element.area for element in self.elements)

    @property
    def centroid(self) -> Point:
        """Centroid of the steel cross-section."""
        area_weighted_centroids_x = sum(element.centroid.x * element.area for element in self.elements)
        area_weighted_centroids_y = sum(element.centroid.y * element.area for element in self.elements)
        centroid_x = area_weighted_centroids_x / self.steel_area
        centroid_y = area_weighted_centroids_y / self.steel_area
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
        distance_to_top = max(point.y for element in self.elements for point in element.cross_section.geometry.exterior.coords) - self.centroid.y
        return self.moment_of_inertia_about_y / distance_to_top

    @property
    def elastic_section_modulus_about_y_negative(self) -> KG_M:
        """Elastic section modulus about the y-axis on the negative z side [mm³]."""
        distance_to_bottom = self.centroid.y - min(point.y for element in self.elements for point in element.cross_section.geometry.exterior.coords)
        return self.moment_of_inertia_about_y / distance_to_bottom

    @property
    def elastic_section_modulus_about_z_positive(self) -> KG_M:
        """Elastic section modulus about the z-axis on the positive y side [mm³]."""
        distance_to_right = max(point.x for element in self.elements for point in element.cross_section.geometry.exterior.coords) - self.centroid.x
        return self.moment_of_inertia_about_z / distance_to_right

    @property
    def elastic_section_modulus_about_z_negative(self) -> KG_M:
        """Elastic section modulus about the z-axis on the negative y side [mm³]."""
        distance_to_left = self.centroid.x - min(point.x for element in self.elements for point in element.cross_section.geometry.exterior.coords)
        return self.moment_of_inertia_about_z / distance_to_left
