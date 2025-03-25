"""Module containing the class definition for a steel cross-section element."""

from dataclasses import dataclass

from shapely import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.general_cross_section import CrossSection
from blueprints.type_alias import KG_M, MM, MM2, MM3, MM4, MPA
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class SteelElement:
    """
    General class for a steel cross-section element.

    Parameters
    ----------
    cross_section : CrossSection
        The cross-section of the steel element.
    material : SteelMaterial
        The material of the steel element.
    name : str
        The name of the steel element.
    """

    cross_section: CrossSection
    material: SteelMaterial
    name: str

    def __post_init__(self) -> None:
        """Check if the material is a SteelMaterial."""
        if not isinstance(self.material, SteelMaterial):
            raise TypeError(f"Expected a SteelMaterial, but got: {type(self.material)}")

    @property
    def area(self) -> MM2:
        """Area of the cross-section [mm²]."""
        return self.cross_section.area

    @property
    def plate_thickness(self) -> MM:
        """Plate thickness of the cross-section [mm]."""
        return self.cross_section.plate_thickness

    @property
    def perimeter(self) -> MM:
        """Perimeter of the cross-section [mm]."""
        return self.cross_section.perimeter

    @property
    def centroid(self) -> Point:
        """Centroid of the cross-section [mm]."""
        return self.cross_section.centroid

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """Moments of inertia of the cross-section [mm⁴]."""
        return self.cross_section.moment_of_inertia_about_y

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """Moments of inertia of the cross-section [mm⁴]."""
        return self.cross_section.moment_of_inertia_about_z

    @property
    def polar_moment_of_inertia(self) -> MM4:
        """Polar moments of inertia of the cross-section [mm⁴]."""
        return self.cross_section.polar_moment_of_inertia

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """Elastic section modulus about the y-axis on the positive z side [mm³]."""
        return self.cross_section.elastic_section_modulus_about_y_positive

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """Elastic section modulus about the y-axis on the negative z side [mm³]."""
        return self.cross_section.elastic_section_modulus_about_y_negative

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """Elastic section modulus about the z-axis on the positive y side [mm³]."""
        return self.cross_section.elastic_section_modulus_about_z_positive

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """Elastic section modulus about the z-axis on the negative y side [mm³]."""
        return self.cross_section.elastic_section_modulus_about_z_negative

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """Plastic section modulus about the y-axis [mm³]."""
        return self.cross_section.plastic_section_modulus_about_y

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """Plastic section modulus about the z-axis [mm³]."""
        return self.cross_section.plastic_section_modulus_about_z

    @property
    def geometry(self) -> dict:
        """Return the geometry of the steel element."""
        return self.cross_section.geometry

    @property
    def vertices(self) -> list[Point]:
        """Return the vertices of the steel element."""
        return self.cross_section.vertices

    @property
    def dotted_mesh(self) -> list:
        """Return the dotted mesh of the steel element."""
        return self.cross_section.dotted_mesh(max_mesh_size=0)

    @property
    def weight_per_meter(self) -> KG_M:
        """
        Calculate the weight per meter of the steel element.

        Returns
        -------
        KG_M
            The weight per meter of the steel element.
        """
        return self.material.density * (self.cross_section.area * MM2_TO_M2)

    @property
    def yield_strength(self) -> MPA:
        """
        Calculate the yield strength of the steel element.

        Returns
        -------
        MPa
            The yield strength of the steel element.
        """
        return self.material.yield_strength(thickness=self.cross_section.plate_thickness)

    @property
    def ultimate_strength(self) -> MPA:
        """
        Calculate the ultimate strength of the steel element.

        Returns
        -------
        MPa
            The ultimate strength of the steel element.
        """
        return self.material.ultimate_strength()
