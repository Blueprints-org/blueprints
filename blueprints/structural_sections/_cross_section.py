"""Cross-section base class."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from operator import methodcaller
from typing import Any

import matplotlib.pyplot as plt
from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties
from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.type_alias import DEG, M3_M, MM, MM2
from blueprints.unit_conversion import MM3_TO_M3


class MeshCreator:
    """Wrapper for the create_mesh method of the Geometry class.

    Refer to `Geometry.create_mesh` for the documentation.
    """

    def __init__(
        self,
        *,
        mesh_sizes: MM2,
        min_angle: DEG | None = None,
        coarse: bool | None = None,
        **kwargs,
    ) -> None:
        params = {
            "mesh_sizes": mesh_sizes,
            "min_angle": min_angle,
            "coarse": coarse,
            **kwargs,
        }
        self._mesh_settings = {key: value for key, value in params.items() if value is not None}
        self._create_mesh = methodcaller("create_mesh", **self.mesh_settings)

    def __call__(self, geometry: Geometry) -> Geometry:
        """Create mesh for the given geometry."""
        return self._create_mesh(geometry)

    @property
    def mesh_settings(self) -> dict[str, Any]:
        """Return the mesh settings as a dictionary."""
        return self._mesh_settings.copy()


class CrossSection(ABC):
    """Base class for cross-section shapes."""

    accuracy = 6
    """Accuracy for rounding polygon coordinates in order to avoid floating point issues.
    This value is used in the derived classes when creating the Shapely Polygon.
    Since the coordinates are in mm, a value of 6 means that the coordinates are rounded to
    the nearest nanometer which is more than sufficient for structural engineering purposes."""

    @property
    def mesh_creator(self) -> MeshCreator:
        """Get the mesh creator for the cross-section."""
        return MeshCreator(mesh_sizes=2.0)

    @property
    def mesh_settings(self) -> dict[str, Any]:
        """Get the mesh settings for the cross-section."""
        return self.mesh_creator.mesh_settings

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
