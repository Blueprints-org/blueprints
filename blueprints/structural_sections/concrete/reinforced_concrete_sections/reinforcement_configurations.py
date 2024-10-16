"""Module for the representation of reinforcement configurations in reinforced concrete sections."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from shapely import LineString

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MM2_M
from blueprints.unit_conversion import M_TO_MM


@dataclass(frozen=True)
class ReinforcementConfiguration(ABC):
    """Base class of all reinforcement configurations.

    Parameters
    ----------
    diameter : MM
        Diameter of the rebar [mm].
    material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
    """

    diameter: MM
    material: ReinforcementSteelMaterial

    def __post_init__(self) -> None:
        """Post initialization of the reinforcement configuration."""
        # diameter is a positive number
        if self.diameter <= 0:
            msg = f"Diameter of the rebar must be a positive number, got {self.diameter}"
            raise ValueError(msg)

    @property
    @abstractmethod
    def area(self) -> MM2:
        """Each reinforcement configuration must have a resulting area."""

    @abstractmethod
    def to_rebars(self, line: LineString) -> list[Rebar]:
        """Convert the reinforcement configuration to a list of rebars.

        Parameters
        ----------
        line : LineString
            Representing the path of the reinforcement in the section.
            Start of the line defines the first rebar of the configuration, end of the line defines the last rebar.

        Returns
        -------
        List[Rebar]
            List of Rebar objects.
        """


@dataclass(kw_only=True, frozen=True)
class ReinforcementByDistance(ReinforcementConfiguration):
    """Representation of a reinforcement configuration given by center-to-center distance.
    For example ⌀16-150, ⌀20-200, ⌀25-250, ⌀32-300, etc.

    Parameters
    ----------
    center_to_center : MM
        Maximum center-to-center distance between rebars [mm].
    """

    center_to_center: MM

    def __post_init__(self) -> None:
        """Post initialization of the reinforcement configuration."""
        super().__post_init__()
        self._validations()

    def _validations(self) -> None:
        """Validation of the reinforcement configuration."""
        # center-to-center is at least the diameter
        if self.center_to_center < self.diameter:
            msg = f"Center-to-center distance must be at least the diameter of the rebar, got {self.center_to_center}"
            raise ValueError(msg)

    @property
    def area(self) -> MM2_M:
        """Area of the reinforcement configuration per meter [mm²/m]."""
        return 0.25 * np.pi * self.diameter**2 * (M_TO_MM / self.center_to_center)

    @property
    def n_rebars_per_meter(self) -> DIMENSIONLESS:
        """Number of rebars per meter [1/m]."""
        return 1.0 * M_TO_MM / self.center_to_center

    def to_rebars(self, line: LineString) -> list[Rebar]:
        """Convert the reinforcement configuration to a list of rebars.

        Parameters
        ----------
        line : LineString
            Representing the path of the reinforcement in the section.
            Start of the line defines the first rebar of the configuration, end of the line defines the last rebar.

        Returns
        -------
        List[Rebar]
            List of Rebar objects.
        """
        # max(int(n), 1) is used to ensure that at least one rebar is placed
        rebars = []

        # define the number of rebars based on the length of the line, minimum 1
        n_rebars = line.length / self.center_to_center
        n_rebars_applied = max(int(n_rebars), 1)

        # calculate the space between the rebars
        side_buffer = (line.length - (n_rebars_applied - 1) * self.center_to_center) / 2
        distances = np.linspace(start=side_buffer, stop=line.length - side_buffer, num=n_rebars_applied)

        # define the representative diameter of the rebar
        reinforcement_area = 0.25 * np.pi * self.diameter**2 * n_rebars
        repr_diameter = np.sqrt(reinforcement_area / (0.25 * np.pi * n_rebars_applied))

        for distance in distances:
            point = line.interpolate(distance)
            rebars.append(
                Rebar(
                    diameter=repr_diameter,
                    x=point.x,
                    y=point.y,
                    material=self.material,
                )
            )
        return rebars

    def __repr__(self) -> str:
        """Representation of the reinforcement configuration."""
        return f"{self.__class__.__name__}|{self!s}|{self.area:.0f} mm²/m"

    def __str__(self) -> str:
        """String representation of the reinforcement configuration."""
        return f"⌀{self.diameter:.0f}-{self.center_to_center:.0f}"


@dataclass(kw_only=True, frozen=True)
class ReinforcementByQuantity(ReinforcementConfiguration):
    """Representation of a reinforcement configuration given by quantity of rebars.
    For example 4⌀16, 6⌀20, 8⌀25, 10⌀32, etc.

    Parameters
    ----------
    n : int
        Amount of longitudinal bars.
    """

    n: int

    def __post_init__(self) -> None:
        """Post initialization of the reinforcement configuration."""
        super().__post_init__()
        self._validations()

    def _validations(self) -> None:
        """Validation of the reinforcement configuration."""
        # check that n is an integer
        if not isinstance(self.n, int):
            msg = f"Number of rebars must be an integer, got {self.n}"
            raise TypeError(msg)

        # check that n is at least 2
        minimum_number_of_rebars = 1
        if self.n < minimum_number_of_rebars:
            msg = f"Number of rebars must be at least {minimum_number_of_rebars}, got {self.n}"
            raise ValueError(msg)

    @property
    def area(self) -> MM2:
        """Area of the reinforcement configuration [mm²]."""
        return 0.25 * np.pi * self.diameter**2 * self.n

    def to_rebars(self, line: LineString) -> list[Rebar]:
        """Convert the reinforcement configuration to a list of rebars.

        Parameters
        ----------
        line : LineString
            Representing the path of the reinforcement in the section.
            Start of the line defines the first rebar of the configuration, end of the line defines the last rebar.

        Returns
        -------
        List[Rebar]
            List of Rebar objects.
        """
        rebars = []
        for index in range(self.n):
            distance = index * line.length / (self.n - 1)
            point = line.interpolate(distance)
            rebars.append(
                Rebar(
                    diameter=self.diameter,
                    x=point.x,
                    y=point.y,
                    material=ReinforcementSteelMaterial(),
                )
            )
        return rebars

    def __repr__(self) -> str:
        """Representation of the reinforcement by quantity."""
        return f"{self.__class__.__name__}|{self!s}|{self.area:.0f} mm²"

    def __str__(self) -> str:
        """String representation of the reinforcement by quantity."""
        return f"{self.n}⌀{self.diameter:.0f}"
