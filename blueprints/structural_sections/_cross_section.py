"""Cross-section base class."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from typing import Any, ClassVar, Self

import matplotlib.pyplot as plt
from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties
from sectionproperties.pre import Geometry
from shapely import Point, Polygon
from shapely.affinity import rotate, translate

from blueprints.type_alias import DEG, M3_M, MM, MM2
from blueprints.unit_conversion import MM3_TO_M3


@dataclass(frozen=True)
class CrossSection(ABC):
    """Base class for cross-section shapes."""

    accuracy: ClassVar[int] = 6
    """Accuracy for rounding polygon coordinates in order to avoid floating point issues.
    This value is used in the derived classes when creating the Shapely Polygon.
    Since the coordinates are in mm, a value of 6 means that the coordinates are rounded to
    the nearest nanometer which is more than sufficient for structural engineering purposes."""

    horizontal_offset: MM = field(default=0.0, kw_only=True)
    """Horizontal offset of the cross-section [mm]. Positive values move the centroid of the cross-section to the right."""
    vertical_offset: MM = field(default=0.0, kw_only=True)
    """Vertical offset of the cross-section [mm]. Positive values move the centroid of the cross-section upwards."""
    rotation: DEG = field(default=0.0, kw_only=True)
    """Rotation of the cross-section [degrees]. Positive values rotate the cross-section counter-clockwise around its centroid."""

    @property
    def mesh_creator(self) -> partial:
        """Get the mesh creator for the cross-section."""
        return partial(Geometry.create_mesh, mesh_sizes=2.0)

    @property
    def mesh_settings(self) -> dict[str, Any]:
        """Get the mesh settings for the cross-section."""
        return self.mesh_creator.keywords

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the cross-section."""

    @property
    @abstractmethod
    def _polygon(self) -> Polygon:
        """Shapely Polygon representing the cross-section not including offsets and rotation.

        Important
        ---------
            This polygon does NOT include the offsets and rotation. Use the `polygon` property to get the correct polygon with
            applied offsets and rotation.
        """

    @property
    def polygon(self) -> Polygon:
        """Shapely Polygon representing the cross-section with applied offsets and rotation."""
        poly = self._polygon

        if self.rotation != 0.0:
            poly = rotate(poly, self.rotation, origin="centroid", use_radians=False)

        if self.horizontal_offset != 0.0 or self.vertical_offset != 0.0:
            poly = translate(
                poly,
                xoff=self.horizontal_offset,
                yoff=self.vertical_offset,
            )

        return poly

    def transform(self, horizontal_offset: MM = 0.0, vertical_offset: MM = 0.0, rotation: DEG = 0.0) -> Self:
        """Return a new cross-section with the applied transformations.

        Parameters
        ----------
        horizontal_offset : MM
            Horizontal offset to apply [mm]. Positive values move the centroid to the right.
        vertical_offset : MM
            Vertical offset to apply [mm]. Positive values move the centroid upwards.
        rotation : DEG
            Rotation to apply [degrees]. Positive values rotate counter-clockwise around the centroid.

        Returns
        -------
        Self
            New cross-section with the applied transformations.
        """
        self_dict = {key: value for key, value in self.__dict__.items() if self.__dataclass_fields__[key].init}
        self_dict["horizontal_offset"] += horizontal_offset
        self_dict["vertical_offset"] += vertical_offset
        self_dict["rotation"] += rotation
        return type(self)(**self_dict)

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
    def cross_section_height(self) -> MM:
        """Height of the cross-section [mm]."""
        return self.polygon.bounds[3] - self.polygon.bounds[1]

    @property
    def cross_section_width(self) -> MM:
        """Width of the cross-section [mm]."""
        return self.polygon.bounds[2] - self.polygon.bounds[0]

    @property
    def volume_per_meter(self) -> M3_M:
        """Total volume of the reinforced cross-section per meter length [m³/m]."""
        length = 1000  # mm
        return self.area * length * MM3_TO_M3

    def _geometry(self) -> Geometry:
        """Geometry object of the cross-section. This is used for section property calculations."""
        geom = Geometry(geom=self.polygon, tol=self.accuracy)
        return self.mesh_creator(geom)

    def _section(self) -> Section:
        """Section object representing the cross-section. This is used for section property calculations."""
        return Section(geometry=self._geometry())

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
        section = self._section()

        if any([geometric, plastic, warping]):
            section.calculate_geometric_properties()
        if warping:
            section.calculate_warping_properties()
        if plastic:
            section.calculate_plastic_properties()

        return section.section_props

    @property
    def plotter(self) -> Callable[[Any], plt.Figure]:
        """Default plotter function for the cross-section."""
        raise AttributeError("No plotter is defined.")

    def plot(self, plotter: Callable[[Any], plt.Figure] | None = None, *args, **kwargs) -> plt.Figure:
        """Plot the cross-section. Making use of the standard plotter.

        Parameters
        ----------
        plotter : Callable[Any, plt.Figure] | None
            The plotter function to use. If None, the default Blueprints plotter of the subclass is used.
        *args
            Additional arguments passed to the plotter.
        **kwargs
            Additional keyword arguments passed to the plotter.
        """
        if plotter is None:
            plotter = self.plotter
        return plotter(
            self,
            *args,
            **kwargs,
        )
