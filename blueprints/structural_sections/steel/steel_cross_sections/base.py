"""Base class of all steel cross-sections."""

from abc import ABC

from shapely.geometry import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.general_cross_section import CrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import KG_M, M3_M, MM2, MM3
from blueprints.unit_conversion import MM3_TO_M3


class SteelCrossSection(ABC):
    """Base class of all steel cross-sections."""

    def __init__(
        self,
        cross_section: CrossSection,
        steel_material: SteelMaterial,
    ) -> None:
        """Initialize the steel cross-section.

        Parameters
        ----------
        cross_section : CrossSection
            Cross-section of the steel element.
        steel_material : SteelMaterial
            Material properties of the steel.
        """
        self.cross_section = cross_section
        self.steel_material = steel_material
        self.elements: list[SteelElement] = []

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
        area_weighted_centroids = sum(element.centroid * element.area for element in self.elements)
        return area_weighted_centroids / self.steel_area

    @property
    def moment_of_inertia_about_y(self) -> KG_M:
        """Moment of inertia about the y-axis per meter length [mm⁴/m]."""
        body_moments_of_inertia = sum(element.moment_of_inertia_about_y for element in self.elements)
        parallel_axis_theorem = sum(element.area * (element.centroid.y - self.centroid) ** 2 for element in self.elements)
        return body_moments_of_inertia + parallel_axis_theorem

    @property
    def moment_of_inertia_about_z(self) -> KG_M:
        """Moment of inertia about the z-axis per meter length [mm⁴/m]."""
        body_moments_of_inertia = sum(element.moment_of_inertia_about_z for element in self.elements)
        parallel_axis_theorem = sum(element.area * (element.centroid.x - self.centroid) ** 2 for element in self.elements)
        return body_moments_of_inertia + parallel_axis_theorem

    @property
    def polar_moment_of_inertia(self) -> KG_M:
        """Polar moment of inertia per meter length [mm⁴/m]."""
        return self.moment_of_inertia_about_y + self.moment_of_inertia_about_z

    @property
    def elastic_section_modulus_about_y_positive(self) -> KG_M:
        """Elastic section modulus about the y-axis on the positive z side [mm³/m]."""
        distance_to_top = max(point.y for point in self.vertices)
        return self.moment_of_inertia_about_y / distance_to_top

    @property
    def elastic_section_modulus_about_y_negative(self) -> KG_M:
        """Elastic section modulus about the y-axis on the negative z side [mm³/m]."""
        distance_to_bottom = min(point.y for point in self.vertices)
        return self.moment_of_inertia_about_y / distance_to_bottom

    @property
    def elastic_section_modulus_about_z_positive(self) -> KG_M:
        """Elastic section modulus about the z-axis on the positive y side [mm³/m]."""
        distance_to_right = max(point.x for point in self.vertices)
        return self.moment_of_inertia_about_z / distance_to_right

    @property
    def elastic_section_modulus_about_z_negative(self) -> KG_M:
        """Elastic section modulus about the z-axis on the negative y side [mm³/m]."""
        distance_to_left = min(point.x for point in self.vertices)
        return self.moment_of_inertia_about_z / distance_to_left

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """Plastic section modulus about the y-axis [mm³]."""
        return 0  # to be added later using mesh

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """Plastic section modulus about the z-axis [mm³]."""
        return 0  # to be added later using mesh

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the cross-section."""
        return [element.cross_section.vertices for element in self.elements]
