"""Reinforced concrete sections module. WORK IN PROGRESS !. NOT READY FOR USE OR REVIEW."""
# ruff: noqa: PLR0913, SLF001, PLR0911, TRY004, C901, PLR0912, PLR0915, PERF203, ARG002

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from shapely import Point, Polygon

from blueprints.geometry.line import Line, Reference
from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.plotter import rcs
from blueprints.type_alias import DIMENSIONLESS, KG_M, KG_M3, M3_M, MM, MM2, MM2_M
from blueprints.unit_conversion import M_TO_MM, MM2_TO_M2, MM3_TO_M3


class Edges(Enum):
    """Enumeration of possible edges of square, rectangular or circular cross-sections. X direction is in the length axis of the cross-section."""

    UPPER_SIDE = "UPPER (+Z)"
    RIGHT_SIDE = "RIGHT (+Y)"
    LOWER_SIDE = "LOWER (-Z)"
    LEFT_SIDE = "LEFT (-Y)"
    ALL_EDGES = "ALL EDGES"


@dataclass
class CoversRectangular:
    """Representation of the covers of a rectangular cross-section."""

    upper: MM = 50.0
    right: MM = 50.0
    lower: MM = 50.0
    left: MM = 50.0

    def get_covers_info(self) -> str:
        """Return a string with the covers of the cross-section."""
        text = "Cover:"

        all_equal = bool(len({self.upper, self.lower, self.right, self.left}) == 1)
        if all_equal:
            return f"Cover: {self.upper:.0f} mm"

        covers = {cover: "" for cover in list({self.upper, self.lower, self.right, self.left})}
        covers[self.upper] = "upper"

        if covers[self.lower]:
            covers[self.lower] += "|lower"
        else:
            covers[self.lower] = "lower"

        if covers[self.left]:
            covers[self.left] += "|left"
        else:
            covers[self.left] = "left"

        if covers[self.right]:
            covers[self.right] += "|right"
        else:
            covers[self.right] = "right"

        for cover, names in covers.items():
            text += f"\n  {names}: {cover:.0f} mm"

        return text


class Stirrup:
    """Representation of the stirrups for a RectangularReinforcedCrossSection.
    Do not use this __init__ directly, but create the object by:
    RectangularReinforcedCrossSection.add_stirrups().

    Parameters
    ----------
    coordinates: list[Point]
        list of nodes that describe the stirrup.
    diameter: float
        Diameter of the stirrup [mm].
    distance: float
        Longitudinal distance between stirrups [mm].
    material: ReinforcementSteelMaterial
        Reinforcement material
    shear_check: bool
        Take stirrup into account in shear check
    torsion_check: bool
        Take stirrup into account in torsion check
    mandrel_diameter_factor: float
        Inner diameter of mandrel as multiple of stirrup diameter [-]
        (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
    anchorage_length: float
        Anchorage length [mm]
    based_on_cover: bool
        Default is False. This helps to categorise stirrups that a created based on the covers present
        in the cross-section.
    """

    counter = 1

    def __init__(
        self,
        coordinates: list[Point],
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: DIMENSIONLESS | None = None,
        anchorage_length: MM = 0.0,
        based_on_cover: bool = False,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
        n_vertices_used: int = 4,
        cover_used: float | None = None,
    ) -> None:
        self.coordinates = coordinates
        self.diameter = diameter
        self.distance = distance
        self.material = material
        self.shear_check = shear_check
        self.torsion_check = torsion_check
        self.anchorage_length = anchorage_length
        self._mandrel_diameter_factor = mandrel_diameter_factor
        self.based_on_cover = based_on_cover
        self._id = Stirrup.counter
        self._relative_start_position = relative_start_position
        self._relative_end_position = relative_end_position
        self.n_vertices_used = n_vertices_used
        self._cover_used = cover_used
        self._amount_of_legs = 2
        Stirrup.counter += 1

    @property
    def mandrel_diameter_factor(self) -> DIMENSIONLESS:
        """Diameter factor of mandrel.
        Standard values given by Dutch Annex Table 8.1Na - NEN-EN 1992-1-1+C2:2011/NB+A1:2020
        (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm).

        Returns
        -------
        float
        """
        if self._mandrel_diameter_factor:
            return self._mandrel_diameter_factor
        return 5.0 if self.diameter > 16.0 else 4.0

    @property
    def as_w(self) -> MM2_M:
        """Total cross-sectional area of the stirrup [mm²/m].

        Returns
        -------
        float
        """
        return self._amount_of_legs * self.area * (M_TO_MM / self.distance)

    @property
    def area(self) -> MM2:
        """Area of the stirrup bar [mm²].

        Returns
        -------
        float
        """
        return 0.25 * np.pi * self.diameter**2

    @property
    def radius(self) -> MM:
        """Radius of the stirrup bar [mm]."""
        return self.diameter / 2

    @property
    def centroid(self) -> Point:
        """Centroid of the stirrup bar [mm]."""
        return Point(
            round(sum(c.x for c in self.coordinates) / len(self.coordinates), 2),
            round(sum(c.y for c in self.coordinates) / len(self.coordinates), 2),
        )

    @property
    def weight_per_meter(self) -> KG_M3:
        """Total mass of the stirrup per meter length in the longitudinal direction (concrete+reinforcement) [kg/m³]
        (Weight of a single stirrup x amount of stirrups present in one meter length).

        Returns
        -------
        float
        """
        polygon = Polygon(self.coordinates)
        return self.material.density * polygon.length * self.area * MM3_TO_M3 * M_TO_MM / self.distance

    @property
    def ctc_distance_legs(self) -> MM:
        """Distance between the legs of the stirrup taken form the center lines of the rebar [mm].

        Returns
        -------
        float
        """
        return max(point.x for point in self.coordinates) - min(point.x for point in self.coordinates)

    @property
    def cover_used(self) -> float:
        """Can be used to store the value of the cover used when adding the stirrup to the cross-section [mm]."""
        if self._cover_used:
            return self._cover_used
        return 0.0

    @property
    def relative_start_position(self) -> DIMENSIONLESS:
        """Relative position of the start of the stirrup."""
        self._validation_relative_position(relative_position=self._relative_start_position)
        return self._relative_start_position

    @property
    def relative_end_position(self) -> float:
        """Relative position of the end of the stirrup."""
        self._validation_relative_position(relative_position=self._relative_end_position)
        return self._relative_end_position

    @staticmethod
    def _validation_relative_position(relative_position: DIMENSIONLESS) -> None:
        """Validation of the relative position of the stirrup."""
        if relative_position < 0.0:
            msg = "Relative position of the stirrup must be greater than or equal to zero"
            raise ValueError(msg)
        if relative_position > 1.0:
            msg = "Relative position of the stirrup must be less than or equal to one"
            raise ValueError(msg)

    def __repr__(self) -> str:
        """Representation of the stirrup."""
        return f"Stirrup (id={self._id})|⌀{self.diameter}/{self.material.name}"


@dataclass
class CircularCrossSection:
    """
    Class to represent a circular cross-section using shapely for geometric calculations.

    Attributes
    ----------
    radius : MM
        The radius of the circular cross-section.
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    name : str | None
        Name of the circular cross-section.
    """

    radius: MM
    x: MM
    y: MM
    name: str | None = None

    def __post_init__(self) -> None:
        """Post-initialization to create a shapely Point and buffer it to create a circular polygon."""
        # Create a Point at the specified origin (x, y)
        self.center = Point(self.x, self.y)
        # Create a circular polygon with the given radius
        self.circle = self.center.buffer(self.radius)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the circular cross-section [mm²].

        Returns
        -------
        float
            The area of the circle.
        """
        return self.circle.area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter (circumference) of the circular cross-section [mm].

        Returns
        -------
        float
            The perimeter of the circle.
        """
        return self.circle.length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the circular cross-section.

        Returns
        -------
        Point
            The centroid of the circle.
        """
        return self.circle.centroid

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the circular cross-section."""
        return list(self.circle.exterior.coords)

    def contains_point(self, x: MM, y: MM) -> bool:
        """
        Check if a point (x, y) is inside the circular cross-section.

        Parameters
        ----------
        x : MM
            The x-coordinate of the point [mm].
        y : MM
            The y-coordinate of the point [mm].

        Returns
        -------
        bool
            True if the point is inside the circle, False otherwise.
        """
        # Check if the point is within the circular polygon
        return self.circle.contains(Point(x, y))


@dataclass
class RectangularCrossSection:
    """
    Class to represent a rectangular cross-section for geometric calculations.

    Attributes
    ----------
    width : MM
        The width of the rectangular cross-section.
    height : MM
        The height of the rectangular cross-section.
    origin : Point
        The centroid of the rectangle, given as a shapely Point. Default is (0, 0).
    """

    width: MM
    height: MM
    origin: Point = field(default_factory=lambda: Point(0, 0))
    _name: str | None = None

    def __post_init__(self) -> None:
        """
        Post-initialization to create a shapely Polygon representing the rectangle
        with the origin as the centroid.
        """
        # Calculate the bottom-left corner coordinates based on the centroid (origin)
        self.x = self.origin.x - self.width / 2
        self.y = self.origin.y - self.height / 2

        # Define the coordinates of the rectangle based on width, height, x, and y
        self.rectangle = Polygon(
            [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)]
        )

    @property
    def name(self) -> str:
        """Name of the rectangular cross-section."""
        if self._name:
            return self._name
        return f"Rectangular {self.width}x{self.height}"

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the rectangular cross-section.

        Returns
        -------
        MM2
            The area of the rectangle.
        """
        return self.rectangle.area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the rectangular cross-section.

        Returns
        -------
        MM
            The perimeter of the rectangle.
        """
        return self.rectangle.length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the rectangular cross-section.

        Returns
        -------
        Point
            The centroid of the rectangle.
        """
        return self.rectangle.centroid

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the rectangular cross-section. Counter-clockwise order starting from the bottom-left corner."""
        return list(self.rectangle.exterior.coords)

    def contains_point(self, x: float, y: float) -> bool:
        """
        Check if a point (x, y) is inside the rectangular cross-section.

        Parameters
        ----------
        x : float
            The x-coordinate of the point.
        y : float
            The y-coordinate of the point.

        Returns
        -------
        bool
            True if the point is inside the rectangle, False otherwise.
        """
        # Check if the point is within the rectangular polygon
        return self.rectangle.contains(Point(x, y))


class Rebar(CircularCrossSection):
    """Representation of a reinforcement bar from a cross-section perspective. For example ⌀16, ⌀20, ⌀25, ⌀32,etc.

    Parameters
    ----------
    diameter : float
        Diameter of the bar (for example: ⌀12, ⌀16, ⌀20, etc.) [mm]
    x : float
        x-coordinate in the cross-section [mm]
    y : float
        y-coordinate in the cross-section [mm]
    material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
    relative_start_position: float
        Relative position of the start of the rebar in the x-direction of the host cross-section [-]
    relative_end_position: float
        Relative position of the end of the rebar in the x-direction of the host cross-section [-]
    name : str | None
        Identification of the rebar (default = ⌀diameter/steel_quality; for example ~ ⌀16/B500B)
    """

    def __init__(
        self,
        diameter: MM,
        x: MM,
        y: MM,
        material: ReinforcementSteelMaterial,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
        name: str | None = None,
    ) -> None:
        """Initialize the Rebar object."""
        super().__init__(radius=diameter / 2, x=x, y=y, name=name)
        self._diameter = diameter
        self.x = x
        self.y = y
        self.material = material
        self._relative_start_position = relative_start_position
        self._relative_end_position = relative_end_position
        self.name = name if name else f"⌀{self.diameter}mm/{self.material.steel_quality.value}"

    @property
    def diameter(self) -> MM:
        """Diameter of the rebar [mm]."""
        if self._diameter <= 0.0:
            msg = "The diameter of the rebar must be greater than zero"
            raise ValueError(msg)
        return self._diameter

    @property
    def weight_per_meter(self) -> KG_M:
        """Unit weight of rebar per meter (G) [kg/m].

        Returns
        -------
        float
            Example: 1.578336149163512 for ⌀16 and normal density of 7850 kg/m3
        """
        return self.material.density * (self.area * MM2_TO_M2)

    @property
    def relative_start_position(self) -> DIMENSIONLESS:
        """Relative position of the start of the rebar."""
        self._validation_relative_position(relative_position=self._relative_start_position)
        return self._relative_start_position

    @property
    def relative_end_position(self) -> float:
        """Relative position of the end of the rebar."""
        self._validation_relative_position(relative_position=self._relative_end_position)
        return self._relative_end_position

    @staticmethod
    def _validation_relative_position(relative_position: DIMENSIONLESS) -> None:
        """Validation of the relative position of the rebar."""
        if relative_position < 0.0:
            msg = "Relative position of the rebar must be greater than or equal to zero"
            raise ValueError(msg)
        if relative_position > 1.0:
            msg = "Relative position of the rebar must be less than or equal to one"
            raise ValueError(msg)


class ReinforcementConfiguration(ABC):
    """Base class of all reinforcement configurations."""

    def __init__(
        self,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> None:
        self._relative_start_position = relative_start_position
        self._relative_end_position = relative_end_position

    @property
    def relative_start_position(self) -> DIMENSIONLESS:
        """Relative position of the start of the reinforcement."""
        self._validation_relative_position(relative_position=self._relative_start_position)
        return self._relative_start_position

    @property
    def relative_end_position(self) -> DIMENSIONLESS:
        """Relative position of the end of the reinforcement."""
        self._validation_relative_position(relative_position=self._relative_end_position)
        return self._relative_end_position

    @property
    @abstractmethod
    def name(self) -> str:
        """Each reinforcement configuration must have a name."""

    @property
    @abstractmethod
    def area(self) -> float:
        """Each reinforcement configuration must have a resulting area."""

    @staticmethod
    def _validation_relative_position(relative_position: DIMENSIONLESS) -> None:
        """Validation of the relative position of the rebar."""
        if relative_position < 0.0:
            msg = "Relative position of the rebar must be greater than or equal to zero"
            raise ValueError(msg)
        if relative_position > 1.0:
            msg = "Relative position of the rebar must be less than or equal to one"
            raise ValueError(msg)


class ReinforcementInLine(ReinforcementConfiguration):
    """Representation of reinforcement in line.

    Parameters
    ----------
    diameter : MM
        Diameter of the rebar [mm].
    n : int
        Number of rebars.
    start_coordinate : Point
        Starting coordinate of the line.
    end_coordinate : Point
        End coordinate of the line.
    material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
    relative_start_position: DIMENSIONLESS
        Relative position of the start of the rebar in the x-direction of the host cross-section [-]
    relative_end_position: DIMENSIONLESS
        Relative position of the end of the rebar in the x-direction of the host cross-section [-]
    name : str | None
        Desired name of the reinforcement configuration.
    """

    def __init__(
        self,
        diameter: MM,
        n: int,
        start_coordinate: Point,
        end_coordinate: Point,
        material: ReinforcementSteelMaterial,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
        name: str | None = None,
    ) -> None:
        super().__init__(relative_start_position=relative_start_position, relative_end_position=relative_end_position)
        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate
        self.diameter = diameter
        self.n = n
        self.material = material
        self._name = name

    @property
    def name(self) -> str:
        """Return the name of the reinforcement configuration."""
        if self._name:
            return self._name
        return f"{self.n}⌀{int(self.diameter)}"

    @property
    def area(self) -> float:
        """Area of the reinforcement configuration [mm²]."""
        return 0.25 * np.pi * self.diameter**2 * int(self.n)

    @property
    def bars(self) -> list[Rebar]:
        """Return a list of evenly spaced longitudinal_rebars from start to end point with an n number of desired points. If n is 1 rebar lies on
        the start point.
        """
        x1 = self.start_coordinate.x
        y1 = self.start_coordinate.y
        x2 = self.end_coordinate.x
        y2 = self.end_coordinate.y
        if self.n > 1:
            internal_points = []
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            evenly_spaced_points = np.linspace(start=0, stop=length, num=self.n, endpoint=True)
            for distance in evenly_spaced_points:
                new_x_coordinate = x1 + (distance / length) * (x2 - x1)
                new_y_coordinate = y1 + (distance / length) * (y2 - y1)
                internal_points.append(Point(new_x_coordinate, new_y_coordinate, 0))
            return [Rebar(diameter=self.diameter, x=point.x, y=point.y, material=self.material) for point in internal_points]

        return [Rebar(diameter=self.diameter, x=x1, y=y1, material=self.material)]

    def __repr__(self) -> str:
        """Representation of the rebar in line."""
        return f"ReinforcementInLine|{self.name}|{int(self.area)}mm²"


class ReinforcementByDistance(ReinforcementConfiguration):
    """Representation of reinforcement by distance.

    Parameters
    ----------
    diameter : MM
        Diameter of the rebar [mm].
    max_distance : MM
        Maximum center-to-center distance between rebars [mm].
    edge : Edges
        Desired edge to add the reinforcement layer to.
    material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
    different_cover: MM
        Use to introduce a different cover of the reinforcement layer which is different from the cross-section cover on the chosen edge [mm]
    cover_as_defined_in_cross_section: bool
        Use the previously defined cover in the cross-section, if False the different_cover will be used to define the cover.
    relative_start_position: DIMENSIONLESS
        Relative position of the start of the rebar in the x-direction of the host cross-section [-]
    relative_end_position: DIMENSIONLESS
        Relative position of the end of the rebar in the x-direction of the host cross-section [-]
    name : str | None
        Desired name of the reinforcement configuration.
    """

    def __init__(
        self,
        diameter: MM,
        max_distance: MM,
        edge: Edges,
        material: ReinforcementSteelMaterial,
        different_cover: MM = 0.0,
        cover_as_defined_in_cross_section: bool = True,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> None:
        super().__init__(relative_start_position=relative_start_position, relative_end_position=relative_end_position)
        self.diameter = diameter
        self.max_distance = max_distance
        self.edge = edge
        self.material = material
        self.cover = different_cover
        self.cover_as_defined_in_cross_section = cover_as_defined_in_cross_section

    @property
    def name(self) -> str:
        """Return the name of the reinforcement configuration."""
        return f"⌀{int(self.diameter)}-{int(self.max_distance)}"

    @property
    def n_rebars_per_meter(self) -> DIMENSIONLESS:
        """Number of rebars per meter [1/m]."""
        return M_TO_MM / self.max_distance

    @property
    def area(self) -> float:
        """Area of the reinforcement configuration per meter [mm²/m]."""
        return 0.25 * np.pi * self.diameter**2 * (M_TO_MM / self.max_distance)

    def __repr__(self) -> str:
        """Representation of the rebar by distance."""
        return f"ReinforcementByDistance|{self.name}|{int(self.area)}mm²/m"


class ReinforcementByQuantity(ReinforcementConfiguration):
    """Representation of reinforcement by quantity.

    Parameters
    ----------
    n : int
        Amount of longitudinal bars.
    diameter : MM
        Diameter of the rebar [mm].
    edge : Edges
        Desired edge to add the reinforcement layer to.
    material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
    different_cover: MM
        Use to introduce a different cover of the reinforcement layer [mm]
    cover_as_defined_in_cross_section: bool
        Use the previously defined cover in the cross-section if False the different_cover will be used to define the cover.
    relative_start_position: DIMENSIONLESS
        Relative position of the start of the rebar in the x-direction of the host cross-section [-]
    relative_end_position: DIMENSIONLESS
        Relative position of the end of the rebar in the x-direction of the host cross-section [-]
    """

    def __init__(
        self,
        n: int,
        diameter: MM,
        edge: Edges,
        material: ReinforcementSteelMaterial,
        different_cover: MM = 0.0,
        cover_as_defined_in_cross_section: bool = True,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
        offset: MM = 0.0,
    ) -> None:
        super().__init__(relative_start_position=relative_start_position, relative_end_position=relative_end_position)
        self.n = n
        self.diameter = diameter
        self.edge = edge
        self.material = material
        self.different_cover = different_cover
        self.cover = different_cover
        self.cover_as_defined_in_cross_section = cover_as_defined_in_cross_section
        self.offset = offset

    @property
    def name(self) -> str:
        """Return the name of the reinforcement configuration."""
        return f"{self.n}⌀{int(self.diameter)}"

    @property
    def area(self) -> float:
        """Area of the reinforcement configuration [mm²]."""
        return 0.25 * np.pi * self.diameter**2 * int(self.n)

    def __repr__(self) -> str:
        """Representation of the reinforcement by quantity."""
        return f"ReinforcementByQuantity|{self.name}|{int(self.area)}mm²"


class CrossSection(Protocol):
    """Protocol for a cross-section."""

    @property
    def name(self) -> str:
        """Name of the cross-section."""

    @property
    def area(self) -> MM2:
        """Area of the cross-section [mm²]."""

    @property
    def perimeter(self) -> MM:
        """Perimeter of the cross-section [mm]."""

    @property
    def centroid(self) -> Point:
        """Centroid of the cross-section [mm]."""

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the cross-section."""

    def contains_point(self, x: MM, y: MM) -> bool:
        """Check if a point (x, y) is inside the cross-section."""


class ReinforcedCrossSection(ABC):
    """Base class of all reinforced cross-sections."""

    def __init__(
        self,
        cross_section: CrossSection,
        concrete_material: ConcreteMaterial,
        name: str | None = None,
    ) -> None:
        self.cross_section = cross_section
        self.concrete_material = concrete_material
        self.single_longitudinal_rebars: list[Rebar] = []
        self.reinforcement_layer_in_line: list[ReinforcementInLine] = []
        self.reinforcement_by_quantity_on_edge: list[ReinforcementByQuantity] = []
        self._reinforcement_by_distance_on_edge: list[ReinforcementByDistance] = []
        self.stirrups: list[Stirrup] = []
        self.name = name if name else f"RCS {self.cross_section.name}"

    @property
    def longitudinal_rebars(self) -> list[Rebar]:
        """Return a list of all longitudinal rebars."""
        rebars = []
        rebars.extend(self.single_longitudinal_rebars)
        if self.reinforcement_layer_in_line:
            for layer in self.reinforcement_layer_in_line:
                rebars.extend(layer.bars)
        if self.reinforcement_by_quantity_on_edge:
            rebars.extend(
                [
                    rebar
                    for layer in self.reinforcement_by_quantity_on_edge
                    for rebar in self.get_rebars_from_reinforcement_configuration(configuration=layer)
                ]
            )
        if self._reinforcement_by_distance_on_edge:
            rebars.extend(
                [
                    rebar
                    for layer in self._reinforcement_by_distance_on_edge
                    for rebar in self.get_rebars_from_reinforcement_configuration(configuration=layer)
                ]
            )
        if rebars:
            for rebar in rebars:
                if not self.cross_section.contains_point(x=rebar.x, y=rebar.y):
                    msg = f"Rebar {rebar.name} is not inside the cross-section."
                    raise ValueError(msg)
        return rebars

    @property
    def reinforcement_weight_longitudinal_bars(self) -> KG_M:
        """Total mass of the longitudinal reinforcement in the cross-section per meter length [kg/m]."""
        return sum(rebar.weight_per_meter for rebar in self.longitudinal_rebars)

    @property
    def reinforcement_weight_stirrups(self) -> KG_M:
        """Total mass of the stirrups' reinforcement in the cross-section per meter length [kg/m]."""
        return sum(stirrup.weight_per_meter for stirrup in self.stirrups)

    @property
    def reinforcement_weight(self) -> KG_M:
        """Total mass of the reinforcement in the cross-section per meter length [kg/m]."""
        return self.reinforcement_weight_longitudinal_bars + self.reinforcement_weight_stirrups

    @property
    def reinforcement_area_longitudinal_bars(self) -> MM2_M:
        """Total area of the longitudinal reinforcement in the cross-section per meter length [mm²/m]."""
        return sum(rebar.area for rebar in self.longitudinal_rebars)

    @property
    def concrete_volume(self) -> M3_M:
        """Total volume of the reinforced cross-section per meter length [m³/m]."""
        length = M_TO_MM
        return self.cross_section.area * length * MM3_TO_M3

    @property
    def weight_per_volume(self) -> KG_M3:
        """Total mass of the cross-section per meter length (concrete_checks+reinforcement) [kg/m³]."""
        return self.reinforcement_weight / self.concrete_volume

    @property
    def reinforcement_area_upper_longitudinal_bars(self) -> MM2_M:
        """Total area of the longitudinal reinforcement in the upper half of the cross-section per meter length [mm²/m]."""
        return sum(rebar.area for rebar in self.longitudinal_rebars if rebar.y > 0)

    @property
    def reinforcement_area_lower_longitudinal_bars(self) -> MM2_M:
        """Total area of the longitudinal reinforcement in the lower half of the cross-section per meter length [mm²/m]."""
        return sum(rebar.area for rebar in self.longitudinal_rebars if rebar.y < 0)

    def add_longitudinal_rebar(
        self,
        diameter: MM,
        x: MM,
        y: MM,
        material: ReinforcementSteelMaterial,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
        name: str | None = None,
    ) -> Rebar:
        """Adds a single reinforced bar to the beam.

        Parameters
        ----------
        diameter: MM
            Diameter of the rebar [mm].
        x: MM
            X coordinate of the bar relative to the origin/centroid of the cross-section [mm].
        y: MM
            Y coordinate of the bar relative to the origin/centroid of the cross-section [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]
        name: str | None
            Desired name of the rebar, may be used to insert other useful information.

        Returns
        -------
        Rebar
            Newly created Rebar
        """
        # initiate the rebar
        rebar = Rebar(
            diameter=diameter,
            x=x,
            y=y,
            material=material,
            name=name,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

        # check if the rebar is inside the cross-section
        self.cross_section.contains_point(x=rebar.x, y=rebar.y)

        # add the rebar to the list of longitudinal rebars
        self.single_longitudinal_rebars.append(rebar)

        return rebar

    def add_longitudinal_reinforcement_in_line(
        self,
        n: int,
        diameter: MM,
        start_coordinate: Point,
        end_coordinate: Point,
        material: ReinforcementSteelMaterial,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> ReinforcementInLine:
        """Adds an in-line layer of reinforced bars to the cross-section.

        Parameters
        ----------
        n: int
            Amount of longitudinal bars.
        diameter: MM
            Diameter of the rebar [mm].
        start_coordinate: Point
            Starting coordinate of the line relative to the origin/centroid of the cross-section.
        end_coordinate: Point
            End coordinate of the line relative to the origin/centroid of the cross-section.
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        ReinforcementInLine
            Newly created ReinforcementInLine
        """
        # check if the start and end point are equal
        if start_coordinate == end_coordinate:
            msg = "Start and end point are equal. Please enter different coordinates."
            raise ValueError(msg)

        # check if the amount of rebars is at least 2
        if n < 2:
            msg = "A minimum of 2 longitudinal rebars are required."
            raise ValueError(msg)

        # check if the start and end point are inside the cross-section
        if not self.cross_section.contains_point(
            x=start_coordinate.x + self.cross_section.centroid.x,
            y=start_coordinate.y + self.cross_section.centroid.y,
        ):
            msg = "Start point of the rebar is not inside the cross-section."
            raise ValueError(msg)
        if not self.cross_section.contains_point(
            x=end_coordinate.x + self.cross_section.centroid.x,
            y=end_coordinate.y + self.cross_section.centroid.y,
        ):
            msg = "End point of the rebar is not inside the cross-section."
            raise ValueError(msg)

        # initiate the reinforcement in line
        reinforcement_in_line = ReinforcementInLine(
            diameter=diameter,
            n=n,
            start_coordinate=start_coordinate,
            end_coordinate=end_coordinate,
            material=material,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

        # add the reinforcement in line to the list of reinforcement layers
        self.reinforcement_layer_in_line.append(reinforcement_in_line)

        return reinforcement_in_line

    def add_longitudinal_reinforcement_by_quantity_on_edge(
        self,
        n: int,
        diameter: MM,
        edge: Edges,
        material: ReinforcementSteelMaterial,
        different_cover: MM = 0.0,
        cover_as_defined_in_cross_section: bool = True,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
        offset: MM = 0.0,
    ) -> ReinforcementByQuantity:
        """Adds a reinforcement layer by quantity to the cross-section.

        Parameters
        ----------
        n: int
            Amount of longitudinal bars [-]. If n=1: the rebar will be placed in the center of the reference line.
        diameter: MM
            Diameter of the rebar [mm].
        edge: Edges
            Desired edge(s) to add the reinforcement layer to.
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
        different_cover: MM
            Use to introduce a different cover of the reinforcement layer [mm]
        cover_as_defined_in_cross_section: bool
            Use the previously defined cover in the cross-section
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]
        offset: MM
            Offset to not cover the entire edge, but only "offset" from the corner. Parallel to the edge provided.

        Returns
        -------
        ReinforcementByQuantity
            Newly created ReinforcementByQuantity
        """
        # initiate the reinforcement by quantity
        reinforcement_by_quantity = ReinforcementByQuantity(
            n=n,
            diameter=diameter,
            edge=edge,
            material=material,
            different_cover=different_cover,
            cover_as_defined_in_cross_section=cover_as_defined_in_cross_section,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
            offset=-offset,
        )

        # add the reinforcement by quantity to the list of reinforcement layers
        self.reinforcement_by_quantity_on_edge.append(reinforcement_by_quantity)

        return reinforcement_by_quantity

    @abstractmethod
    def _get_rebars_from_reinforcement_by_quantity(self, configuration: ReinforcementByQuantity) -> list[Rebar]:
        """Each type of reinforced cross-sections needs to incorporate a way to make a list of rebars out of the present
        reinforcement by quantity configuration inside the cross-section.
        """

    @abstractmethod
    def _get_rebars_from_reinforcement_by_distance(self, configuration: ReinforcementByDistance) -> list[Rebar]:
        """Each type of reinforced cross-sections needs to incorporate a way to make a list of rebars out of the present
        reinforcement by distance configuration inside the cross-section.
        """

    def get_rebars_from_reinforcement_configuration(self, configuration: ReinforcementByQuantity | ReinforcementByDistance) -> list[Rebar]:
        """Gets a list of rebars from a reinforcement configuration."""
        if not isinstance(configuration, (ReinforcementByQuantity, ReinforcementByDistance)):
            msg = f"{configuration} is not a valid input for _get_rebars_from_reinforcement_configuration()"
            raise ValueError(msg)
        if isinstance(configuration, ReinforcementByDistance):
            return self._get_rebars_from_reinforcement_by_distance(configuration=configuration)
        return self._get_rebars_from_reinforcement_by_quantity(configuration=configuration)

    @abstractmethod
    def plot(self) -> plt.Figure | go.Figure:
        """
        Each type of reinforced cross-sections needs to incorporate its own representation of a plot.
        This could be a matplotlib or plotly figure.
        """


class RectangularReinforcedCrossSection(ReinforcedCrossSection):
    """Representation of a reinforced rectangular concrete cross-section like a beam.

    Parameters
    ----------
    width: MM
        Width of the reinforced cross-section [mm]
    height: MM
        Height of the reinforced cross-section [mm]
    covers: CoversRectangular
        Covers of the cross-section.
    concrete_material: ConcreteMaterial
        Representation of the properties of concrete suitable for use with NEN-EN 1992-1-1
    steel_material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
    name : str
        Name of the reinforced cross-section.
    """

    def __init__(
        self,
        width: MM,
        height: MM,
        covers: CoversRectangular,
        concrete_material: ConcreteMaterial,
        steel_material: ReinforcementSteelMaterial,
        name: str | None = None,
    ) -> None:
        super().__init__(
            cross_section=RectangularCrossSection(width=width, height=height),
            concrete_material=concrete_material,
        )
        self.steel_material = steel_material
        self.width = width
        self.height = height
        self.name = (
            name
            if name
            else f"RectangularReinforcedCrossSection {self.width}x{self.height}mm|{self.concrete_material.name}|{self.steel_material.name}"
        )
        self.covers = covers
        self.plotter = rcs.RectangularCrossSectionPlotter(self)

    def set_covers(
        self,
        upper_edge: MM | None = None,
        right_edge: MM | None = None,
        lower_edge: MM | None = None,
        left_edge: MM | None = None,
    ) -> None:
        """Method to change covers in the cross-section.

        Parameters
        ----------
        upper_edge: MM | None, default None
            New reinforcement coverage for the upper side of the cross-section [mm]
        right_edge: MM | None, default None
            New reinforcement coverage for the right side of the cross-section [mm]
        lower_edge: MM | None, default None
            New reinforcement coverage for the lower side of the cross-section [mm]
        left_edge: MM | None, default None
            New reinforcement coverage for the left side of the cross-section [mm]
        """
        self.covers.upper = upper_edge if upper_edge else self.covers.upper
        self.covers.right = right_edge if right_edge else self.covers.right
        self.covers.lower = lower_edge if lower_edge else self.covers.lower
        self.covers.left = left_edge if left_edge else self.covers.left

    def add_stirrups(
        self,
        coordinates: list[Point],
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: DIMENSIONLESS | None = None,
        anchorage_length: MM = 0.0,
        based_on_cover: bool = False,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> Stirrup:
        """Add a single stirrup to the reinforced cross-section based on given coordinates.

        Parameters
        ----------
        coordinates: list[Point]
            list of (x,y) coordinates to describe the stirrup relative to the centroid point of the cross-section. [mm]
        diameter: MM
            Diameter of the stirrups [mm].
        distance: MM
            Longitudinal distance between stirrups [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
        shear_check: bool
            Take stirrup into account in shear check
        torsion_check: bool
            Take stirrup into account in torsion check
        mandrel_diameter_factor: DIMENSIONLESS
            Inner diameter of mandrel as multiple of stirrup diameter [-]
            (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
        anchorage_length: MM
            Anchorage length [mm]
        based_on_cover: bool
            Default is False. This helps to categorise stirrups that are created based on the covers present
            in the cross-section.
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        Stirrup
            Newly created Stirrup
        """
        # initiate the stirrup
        stirrup = Stirrup(
            coordinates=coordinates,
            diameter=diameter,
            distance=distance,
            material=material,
            shear_check=shear_check,
            torsion_check=torsion_check,
            mandrel_diameter_factor=mandrel_diameter_factor,
            anchorage_length=anchorage_length,
            based_on_cover=based_on_cover,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

        # add the stirrup to the list of stirrups
        self.stirrups.append(stirrup)

        return stirrup

    def add_stirrup_along_edges(
        self,
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: float | None = None,
        anchorage_length: MM = 0.0,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> Stirrup:
        """Add stirrups to the reinforced cross-section based on the present covers.

        (No coordinates are needed for the creation of this stirrup.)

        Parameters
        ----------
        diameter: MM
            Diameter of the stirrups [mm].
        distance: MM
            Longitudinal distance between stirrups [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
        shear_check: bool
            Take stirrup into account in shear check
        torsion_check: bool
            Take stirrup into account in torsion check
        mandrel_diameter_factor: DIMENSIONLESS
            Inner diameter of mandrel as multiple of stirrup diameter [-]
            (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
        anchorage_length: MM
            Anchorage length [mm]
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        Stirrup
            Newly created Stirrup
        """
        _max_x = max(x for x, _ in self.cross_section.vertices)
        _min_x = min(x for x, _ in self.cross_section.vertices)
        _min_y = min(y for _, y in self.cross_section.vertices)
        _max_y = max(y for _, y in self.cross_section.vertices)

        _left_bottom_corner = Point(_min_x + self.covers.left + (diameter / 2), _min_y + self.covers.lower + (diameter / 2))
        _left_top_corner = Point(_min_x + self.covers.left + (diameter / 2), _max_y - self.covers.upper - (diameter / 2))
        _right_top_corner = Point(_max_x - self.covers.right - (diameter / 2), _max_y - self.covers.upper - (diameter / 2))
        _right_bottom_corner = Point(_max_x - self.covers.right - (diameter / 2), _min_y + self.covers.lower + (diameter / 2))

        return self.add_stirrups(
            coordinates=[_left_top_corner, _left_bottom_corner, _right_bottom_corner, _right_top_corner],
            diameter=diameter,
            distance=distance,
            material=material,
            shear_check=shear_check,
            torsion_check=torsion_check,
            mandrel_diameter_factor=mandrel_diameter_factor,
            anchorage_length=anchorage_length,
            based_on_cover=True,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

    def add_stirrup_in_center(
        self,
        width: MM,
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: float | None = None,
        anchorage_length: MM = 0.0,
        relative_start_position: DIMENSIONLESS = 0.0,
        relative_end_position: DIMENSIONLESS = 1.0,
    ) -> Stirrup:
        """Add stirrups to the center of the reinforced cross-section based on a given width (ctc of the legs).

        (No coordinates are needed for the creation of this stirrup.)

        Parameters
        ----------
        width: MM
            Total width of the stirrup taken from the center lines of the legs [mm].
        diameter: MM
            Diameter of the stirrups [mm].
        distance: MM
            Longitudinal distance between stirrups [mm].
        material : ReinforcementSteelMaterial
            Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1
        shear_check: bool
            Take stirrup into account in shear check
        torsion_check: bool
            Take stirrup into account in torsion check
        mandrel_diameter_factor: DIMENSIONLESS
            Inner diameter of mandrel as multiple of stirrup diameter [-]
            (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
        anchorage_length: MM
            Anchorage length [mm]
        relative_start_position: DIMENSIONLESS
            Relative position of the start of the rebar in the x-direction of the host cross-section [-]
        relative_end_position: DIMENSIONLESS
            Relative position of the end of the rebar in the x-direction of the host cross-section [-]

        Returns
        -------
        Stirrup
            Newly created Stirrup
        """
        _min_y = min(y for _, y in self.cross_section.vertices)
        _max_y = max(y for _, y in self.cross_section.vertices)

        _left_bottom_corner = Point(-width / 2, _min_y + self.covers.lower + (diameter / 2))
        _left_top_corner = Point(-width / 2, _max_y - self.covers.upper - (diameter / 2))
        _right_top_corner = Point(width / 2, _max_y - self.covers.upper - (diameter / 2))
        _right_bottom_corner = Point(width / 2, _min_y + self.covers.lower + (diameter / 2))

        return self.add_stirrups(
            coordinates=[_left_top_corner, _left_bottom_corner, _right_bottom_corner, _right_top_corner],
            diameter=diameter,
            distance=distance,
            material=material,
            shear_check=shear_check,
            torsion_check=torsion_check,
            mandrel_diameter_factor=mandrel_diameter_factor,
            anchorage_length=anchorage_length,
            based_on_cover=False,
            relative_start_position=relative_start_position,
            relative_end_position=relative_end_position,
        )

    def _get_reference_line_by_edge(
        self,
        edge: Edges,
        diameter: float,
        different_cover: float = 0.0,
        cover_as_defined_in_cross_section: bool = True,
    ) -> Line:
        """Get a reference line for a reinforcement layer taking into account to desired edge,
         present covers and presence of stirrups in the cross-section.

        Parameters
        ----------
        edge: Edges
            Desired edge of the cross-section. (Edges.ALL_EDGES is not supported)
        diameter: float
            Diameter of the rebars in the layer [mm]
        different_cover: float
            Use to introduce a different cover of the reinforcement layer [mm]
        cover_as_defined_in_cross_section: bool
            Use the previously defined cover in the cross-section

        Returns
        -------
        Line
        """
        if edge == Edges.ALL_EDGES:
            msg = "This operation is currently not supported for Edges.ALL_EDGES"
            raise NotImplementedError(msg)
        if diameter < 1:
            msg = "Diameter must be greater than 1"
            raise ValueError(msg)

        # get the vertices of the shape
        lower_left, lower_right, upper_right, upper_left, _ = self.cross_section.vertices

        # start of the reference line is a half diameter from the reinforcement cover eventually increased by the diameter of the biggest stirrup
        half_diameter = diameter / 2
        if self.stirrups:
            half_diameter += max(stirrup.diameter for stirrup in self.stirrups)

        # define the start and end point of the reference line for the desired reinforcement configuration (default = upper side)
        reinforcement_cover = self.covers.upper if cover_as_defined_in_cross_section else max(different_cover, 0.0)
        match edge:
            case Edges.UPPER_SIDE:
                x1, y1 = upper_left
                x2, y2 = upper_right
                first_point = Point(x1 + self.covers.left + half_diameter, y1 - reinforcement_cover - half_diameter, 0)
                second_point = Point(x2 - self.covers.right - half_diameter, y2 - reinforcement_cover - half_diameter, 0)
            case Edges.RIGHT_SIDE:
                reinforcement_cover = self.covers.right if cover_as_defined_in_cross_section else max(different_cover, 0.0)
                x1, y1 = upper_right
                x2, y2 = lower_right
                first_point = Point(x1 - reinforcement_cover - half_diameter, y1 - self.covers.upper - half_diameter, 0)
                second_point = Point(x2 - reinforcement_cover - half_diameter, y2 + self.covers.lower + half_diameter, 0)
            case Edges.LOWER_SIDE:
                reinforcement_cover = self.covers.lower if cover_as_defined_in_cross_section else max(different_cover, 0.0)
                x1, y1 = lower_right
                x2, y2 = lower_left
                first_point = Point(x1 - self.covers.right - half_diameter, y1 + reinforcement_cover + half_diameter, 0)
                second_point = Point(x2 + self.covers.left + half_diameter, y2 + reinforcement_cover + half_diameter, 0)
            case Edges.LEFT_SIDE:
                reinforcement_cover = self.covers.left if cover_as_defined_in_cross_section else max(different_cover, 0.0)
                x1, y1 = lower_left
                x2, y2 = upper_left
                first_point = Point(x1 + reinforcement_cover + half_diameter, y1 + self.covers.lower + half_diameter, 0)
                second_point = Point(x2 + reinforcement_cover + half_diameter, y2 - self.covers.upper - half_diameter, 0)
            case _:
                msg = "This operation is currently not supported for Edges.ALL_EDGES"
                raise NotImplementedError(msg)

        return Line(start_point=first_point, end_point=second_point)

    def _get_rebars_from_reinforcement_by_quantity(self, configuration: ReinforcementByQuantity) -> list[Rebar]:
        """Gets a list of the rebars for the desired reinforcement layer configuration taking into account the properties of the cross-section.

        Parameters
        ----------
        configuration: ReinforcementByQuantity
            Reinforcement layer by quantity (example= 5⌀20).

        Returns
        -------
        list[Rebar]
        """
        reference_line = self._get_reference_line_by_edge(
            edge=configuration.edge,
            diameter=configuration.diameter,
            different_cover=configuration.cover,
            cover_as_defined_in_cross_section=configuration.cover_as_defined_in_cross_section,
        )
        reference_line.extend(extra_length=configuration.offset, direction=Reference.START)
        reference_line.extend(extra_length=configuration.offset, direction=Reference.END)
        if configuration.n == 1:
            mid_point = reference_line.midpoint
            return [Rebar(diameter=configuration.diameter, material=configuration.material, x=mid_point.x, y=mid_point.y)]
        return [
            Rebar(diameter=configuration.diameter, x=point.x, y=point.y, material=configuration.material)
            for point in reference_line.get_evenly_spaced_points(n=configuration.n)
        ]

    def _get_rebars_from_reinforcement_by_distance(self, configuration: ReinforcementByDistance) -> list[Rebar]:
        """Raises not implemented error."""
        msg = (
            "Reinforcement configurations by distance (ReinforcementByDistance) are not supported for "
            "RectangularReinforcedCrossSection, Use a OneWaySlabReinforcedCrossSection instead"
        )
        raise NotImplementedError(msg)

    def plot(
        self,
        figsize: tuple[float, float] = (15.0, 8.0),
        title: str | None = None,
        font_size_title: float = 18.0,
        font_size_legend: float = 10.0,
        include_legend: bool = True,
        font_size_dimension: float = 12.0,
        custom_text_legend: str | None = None,
        custom_text_width: str | None = None,
        custom_text_height: str | None = None,
        offset_line_width: float = 1.25,
        offset_line_height: float = 1.2,
        show: bool = False,
        axes_i: int = 0,
    ) -> plt.Figure:
        """Get matplotlib figure plot of the reinforced cross-section including longitudinal_rebars and stirrups.

        Parameters
        ----------
        figsize: tuple[float, float]
            Size of the plot window.
        title: str
            Title of the plot.
        font_size_title: float
            Font size of the title.
        font_size_legend: float
            Font size of the legend.
        include_legend: bool
            Include legend in the plot.
        font_size_dimension: float
            Font size of the dimensions.
        custom_text_legend: str
            Custom text for the legend.
        custom_text_width: str
            Custom text for the width dimension. Replaces the width of the cross-section with the custom text.
        custom_text_height: str
            Custom text for the height dimension. Replaces the height of the cross-section with the custom text.
        offset_line_width: float
            Offset of the width line.
        offset_line_height: float
            Offset of the height line.
        show: bool
            Show the plot.
        axes_i: int
            Index of the axes to plot on. Default is 0.

        Returns
        -------
        plt.Figure
        """
        return self.plotter.plot(
            figsize=figsize,
            title=title,
            font_size_title=font_size_title,
            font_size_legend=font_size_legend,
            include_legend=include_legend,
            font_size_dimension=font_size_dimension,
            custom_text_legend=custom_text_legend,
            custom_text_width=custom_text_width,
            custom_text_height=custom_text_height,
            offset_line_width=offset_line_width,
            offset_line_height=offset_line_height,
            show=show,
            axes_i=axes_i,
        )


if __name__ == "__main__":
    # maak betonmateriaal aan
    concrete = ConcreteMaterial()

    # maak staalmateriaal aan
    steel = ReinforcementSteelMaterial(steel_quality=ReinforcementSteelQuality.B500B)

    # maak doorsnede aan
    cs = RectangularReinforcedCrossSection(
        width=1000,
        height=800,
        covers=CoversRectangular(),
        concrete_material=concrete,
        steel_material=steel,
    )

    # pas dekkingen aan in de huidige doorsnede
    cs.set_covers(upper_edge=60, lower_edge=45)

    # voeg wapening per zijde toe aan de doorsnede (n⌀Diameter)
    cs.add_longitudinal_reinforcement_by_quantity_on_edge(
        n=5,
        diameter=14,
        edge=Edges.UPPER_SIDE,
        material=steel,
    )
    cs.add_longitudinal_reinforcement_by_quantity_on_edge(
        n=4,
        diameter=20,
        edge=Edges.LOWER_SIDE,
        material=steel,
    )
    cs.add_longitudinal_reinforcement_by_quantity_on_edge(
        n=3,
        diameter=11,
        edge=Edges.LEFT_SIDE,
        material=steel,
    )
    cs.add_longitudinal_reinforcement_by_quantity_on_edge(
        n=5,
        diameter=9,
        edge=Edges.RIGHT_SIDE,
        material=steel,
    )

    # Beugels
    cs.add_stirrup_along_edges(
        diameter=8,
        distance=150,
        material=steel,
    )
    cs.add_stirrup_in_center(
        width=500,
        diameter=10,
        distance=170,
        material=steel,
    )

    # voeg wapening toe aan de doorsnede (n⌀Diameter)
    cs.add_longitudinal_reinforcement_in_line(
        n=7,
        diameter=8,
        start_coordinate=Point(-372, -274),
        end_coordinate=Point(370, 73),
        material=steel,
    )

    # Lose wapeningsstaven
    cs.add_longitudinal_rebar(
        diameter=40,
        x=0,
        y=0,
        material=steel,
    )

    cs.plot(show=True)
