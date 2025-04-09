"""General cross-section shape."""

from typing import Protocol

from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


class CrossSection(Protocol):
    """Protocol for a cross-section."""

    @property
    def name(self) -> str:
        """Name of the cross-section."""

    @property
    def geometry(self) -> Polygon:
        """Shapely Polygon representing the cross-section."""

    @property
    def area(self) -> MM2:
        """Area of the cross-section [mm²]."""

    @property
    def plate_thickness(self) -> MM:
        """Plate thickness of the cross-section [mm]."""

    @property
    def perimeter(self) -> MM:
        """Perimeter of the cross-section [mm]."""

    @property
    def centroid(self) -> Point:
        """Centroid of the cross-section [mm]."""

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """Moments of inertia of the cross-section [mm⁴]."""

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """Moments of inertia of the cross-section [mm⁴]."""

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """Elastic section modulus about the y-axis on the positive z side [mm³]."""

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """Elastic section modulus about the y-axis on the negative z side [mm³]."""

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """Elastic section modulus about the z-axis on the positive y side [mm³]."""

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """Elastic section modulus about the z-axis on the negative y side [mm³]."""

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """Plastic section modulus about the y-axis [mm³]."""

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """Plastic section modulus about the z-axis [mm³]."""
