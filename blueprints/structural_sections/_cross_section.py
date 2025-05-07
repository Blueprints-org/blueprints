"""Cross-section base class."""

from abc import ABC, abstractmethod

from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties
from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


class CrossSection(ABC):
    """Base class for cross-section shapes."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the cross-section."""

    @property
    @abstractmethod
    def polygon(self) -> Polygon:
        """Shapely Polygon representing the cross-section."""

    @property
    def area(self) -> MM2:
        """Area of the cross-section [mm²].

        When using circular cross-sections, the area is an approximation of the area of the polygon.
        The area is calculated using the `area` property of the Shapely Polygon.

        In case you need an exact answer then you need to override this method in the derived class.
        """
        return self.polygon.area

    @property
    def perimeter(self) -> MM:
        """Perimeter of the cross-section [mm]."""
        return self.polygon.length

    @property
    def centroid(self) -> Point:
        """Centroid of the cross-section [mm]."""
        return self.polygon.centroid

    @property
    @abstractmethod
    def moment_of_inertia_about_y(self) -> MM4:
        """Moments of inertia of the cross-section [mm⁴]."""

    @property
    @abstractmethod
    def moment_of_inertia_about_z(self) -> MM4:
        """Moments of inertia of the cross-section [mm⁴]."""

    @property
    @abstractmethod
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """Elastic section modulus about the y-axis on the positive z side [mm³]."""

    @property
    @abstractmethod
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """Elastic section modulus about the y-axis on the negative z side [mm³]."""

    @property
    @abstractmethod
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """Elastic section modulus about the z-axis on the positive y side [mm³]."""

    @property
    @abstractmethod
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """Elastic section modulus about the z-axis on the negative y side [mm³]."""

    @property
    @abstractmethod
    def plastic_section_modulus_about_y(self) -> MM3 | None:
        """Plastic section modulus about the y-axis [mm³]."""

    @property
    @abstractmethod
    def plastic_section_modulus_about_z(self) -> MM3 | None:
        """Plastic section modulus about the z-axis [mm³]."""

    def geometry(self, mesh_size: MM | None = None) -> Geometry:
        """Geometry of the cross-section.

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
        return Section(geometry=self.geometry())

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
