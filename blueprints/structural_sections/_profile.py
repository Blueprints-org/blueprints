"""Profile base class."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from functools import cached_property, partial
from typing import Any, ClassVar, Self

import matplotlib.pyplot as plt
from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties
from sectionproperties.post.stress_post import StressPost
from sectionproperties.pre import Geometry
from shapely import Point, Polygon
from shapely.affinity import rotate, translate

from blueprints.type_alias import DEG, KN, KNM, M3_M, MM, MM2
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM, M_TO_MM, MM3_TO_M3


@dataclass(frozen=True)
class Profile(ABC):
    """Base class for shapes of structural cross-sections."""

    accuracy: ClassVar[int] = 6
    """Accuracy for rounding polygon coordinates in order to avoid floating point issues.
    This value is used in the derived classes when creating the Shapely Polygon.
    Since the coordinates are in mm, a value of 6 means that the coordinates are rounded to
    the nearest nanometer which is more than sufficient for structural engineering purposes."""

    horizontal_offset: MM = field(default=0.0, kw_only=True)
    """Horizontal offset of the profile [mm]. Positive values move the centroid of the profile to the right."""
    vertical_offset: MM = field(default=0.0, kw_only=True)
    """Vertical offset of the profile [mm]. Positive values move the centroid of the profile upwards."""
    rotation: DEG = field(default=0.0, kw_only=True)
    """Rotation of the profile [degrees]. Positive values rotate the profile counter-clockwise around its centroid."""

    @property
    def mesh_creator(self) -> partial:
        """Get the mesh creator for the profile."""
        return partial(Geometry.create_mesh, mesh_sizes=2.0)

    @property
    def mesh_settings(self) -> dict[str, Any]:
        """Get the mesh settings for the profile."""
        return self.mesh_creator.keywords

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the profile."""

    @property
    @abstractmethod
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""

    @property
    @abstractmethod
    def _polygon(self) -> Polygon:
        """Shapely Polygon representing the profile not including offsets and rotation.

        Important
        ---------
            This polygon does NOT include the offsets and rotation. Use the `polygon` property to get the correct polygon with
            applied offsets and rotation.
        """

    @property
    def polygon(self) -> Polygon:
        """Shapely Polygon representing the profile with applied offsets and rotation."""
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
        """Return a new profile with the applied transformations.

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
            New profile with the applied transformations.
        """
        return replace(
            self,
            horizontal_offset=self.horizontal_offset + horizontal_offset,
            vertical_offset=self.vertical_offset + vertical_offset,
            rotation=self.rotation + rotation,
        )

    @property
    def area(self) -> MM2:
        """Area of the profile [mm²].

        When using circular profiles, the area is an approximation of the area of the polygon.
        The area is calculated using the `area` property of the Shapely Polygon.

        In case you need an exact answer then you need to override this method in the derived class.
        """
        return self.polygon.area

    @property
    def perimeter(self) -> MM:
        """Perimeter of the profile [mm]."""
        return self.polygon.length

    @property
    def centroid(self) -> Point:
        """Centroid of the profile [mm]."""
        return self.polygon.centroid

    @property
    def profile_height(self) -> MM:
        """Height of the profile [mm]."""
        return self.polygon.bounds[3] - self.polygon.bounds[1]

    @property
    def profile_width(self) -> MM:
        """Width of the profile [mm]."""
        return self.polygon.bounds[2] - self.polygon.bounds[0]

    @property
    def volume_per_meter(self) -> M3_M:
        """Total volume of the reinforced profile per meter length [m³/m]."""
        length = 1 * M_TO_MM  # mm
        return self.area * length * MM3_TO_M3

    def _geometry(self) -> Geometry:
        """Geometry object of the profile. This is used for section property calculations."""
        geom = Geometry(geom=self.polygon, tol=self.accuracy)
        return self.mesh_creator(geom)

    def _section(self) -> Section:
        """Section object representing the profile. This is used for section property calculations."""
        return Section(geometry=self._geometry())

    def section_properties(
        self,
        geometric: bool = True,
        plastic: bool = True,
        warping: bool = False,
    ) -> SectionProperties:
        """Calculate and return the section properties of the profile.

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
        """Default plotter function for the profile."""
        raise AttributeError("No plotter is defined.")

    def calculate_stress(self, n: KN = 0, v_y: KN = 0, v_z: KN = 0, m_x: KNM = 0, m_y: KNM = 0, m_z: KNM = 0) -> StressPost:
        """Calculate the stress distribution for the profile given internal forces.

        # Coordinate System Blueprints:
        #     z (vertical, usually strong axis)
        #         ↑
        #         |     x (longitudinal beam direction, into screen)
        #         |    ↗
        #         |   /
        #         |  /
        #         | /
        #         |/
        #   ←-----O
        #    y (horizontal/side, usually weak axis)

        Parameters
        ----------
        n : KN
            Axial force [kN], positive for tension, negative for compression. Default is 0 kN (no axial force).
        v_y : KN
            Shear force in the y-direction [kN], positive for leftward, negative for rightward shear. Default is 0 kN (no shear force).
        v_z : KN
            Shear force in the z-direction [kN], positive for upward, negative for downward shear. Default is 0 kN (no shear force).
        m_x : KNM
            Torsional moment [kNm], positive for y to z, negative for z to y. Default is 0 kNm (no torsion).
        m_y : KNM
            Bending moment about the y-axis [kNm], positive for z to x, negative for x to z. Default is 0 kNm (no bending moment about y-axis).
        m_z : KNM
            Bending moment about the z-axis [kNm], positive for x to y, negative for y to x. Default is 0 kNm (no bending moment about z-axis).

        Returns
        -------
        Callable[..., StressPost]
            A function that calculates the stress distribution when called.
        """
        section = self._section()
        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        # Note: The mapping of internal forces to sectionproperties parameters
        # Blueprints uses x for longitudinal axis, y for horizontal, z for vertical
        # sectionproperties uses x for horizontal, y for vertical, z for longitudinal

        # Coordinate System Blueprints:                              Coordinate System SectionProperties:
        #     z (vertical, usually strong axis)                          y (vertical, usually strong axis)
        #         ↑                                                        ↑
        #         |     x (longitudinal beam direction, into screen)       |      z (longitudinal beam direction, into screen)
        #         |    ↗                                                   |    ↗
        #         |   /                                                    |   /
        #         |  /                                                     |  /
        #         | /                                                      | /
        #         |/                                                       |/
        #   ←-----O                                                        O------>
        #    y (horizontal/side, usually weak axis)                      x (horizontal/side, usually weak axis)

        return section.calculate_stress(
            n=float(n) * KN_TO_N,
            vx=-float(v_y) * KN_TO_N,
            vy=float(v_z) * KN_TO_N,
            mxx=-float(m_y) * KNM_TO_NMM,
            myy=float(m_z) * KNM_TO_NMM,
            mzz=float(m_x) * KNM_TO_NMM,
        )

    @cached_property
    def unit_stress(self) -> dict[str, Any]:
        """Calculate the unit stress distribution for the profile.

        This property is cached, so the calculation is performed only once per instance.

        Returns
        -------
        StressPost
            The unit stress distribution for the profile.
        """
        return self.calculate_stress(1, 1, 1, 1, 1, 1).get_stress()[0]

    def plot(self, plotter: Callable[[Any], plt.Figure] | None = None, *args, **kwargs) -> plt.Figure:
        """Plot the profile. Making use of the standard plotter.

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
