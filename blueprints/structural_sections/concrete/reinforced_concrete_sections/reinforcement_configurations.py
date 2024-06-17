"""Module for the representation of reinforcement configurations in reinforced concrete sections."""

from abc import ABC, abstractmethod

import numpy as np
from shapely import Point

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_sections_shapes import Edges
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.unit_conversion import M_TO_MM


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
