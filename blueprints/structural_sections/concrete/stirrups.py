"""Stirrups module."""

import numpy as np
from shapely import Point, Polygon
from shapely.geometry.polygon import orient

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MM2, MM2_M, RATIO
from blueprints.unit_conversion import M_TO_MM, MM3_TO_M3

STIRRUP_COLOR = (0.412, 0.412, 0.412)


class StirrupConfiguration:
    """Representation of a stirrup configuration.

    Parameters
    ----------
    geometry: Polygon
        Line that represents the center-line of the stirrup configuration (clockwise or counterclockwise).
    diameter: MM
        Diameter of the rebar making the stirrup [mm].
    distance: MM
        Longitudinal distance between stirrups [mm].
    material: ReinforcementSteelMaterial
        Reinforcement material.
    shear_check: bool
        Take stirrup into account in shear check
    torsion_check: bool
        Take stirrup into account in torsion check
    mandrel_diameter_factor: MM
        Inner diameter of mandrel as multiple of stirrup diameter [-]
        (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm) Tabel 8.1Na NEN-EN 1992-1-1 Dutch National Annex.
    anchorage_length: MM
        Anchorage length [mm]
    based_on_cover: bool
        Default is False. This helps to categorise stirrups that a created based on the covers present in the cross-section.
    relative_start_position: RATIO
        Relative position of the start of the stirrup configuration inside the cross-section (longitudinal direction). Value between 0 and 1.
        Default is 0 (start).
    relative_end_position: RATIO
        Relative position of the end of the stirrup configuration inside the cross-section (longitudinal direction). Value between 0 and 1. Default
        is 1 (end).
    """

    counter = 1

    def __init__(  # noqa: PLR0913
        self,
        geometry: Polygon,
        diameter: MM,
        distance: MM,
        material: ReinforcementSteelMaterial,
        shear_check: bool = True,
        torsion_check: bool = True,
        mandrel_diameter_factor: DIMENSIONLESS | None = None,
        anchorage_length: MM = 0.0,
        based_on_cover: bool = False,
        relative_start_position: RATIO = 0.0,
        relative_end_position: RATIO = 1.0,
        n_vertices_used: int = 4,
        cover_used: MM | None = None,
    ) -> None:
        """Initialisation of the stirrup."""
        self.geometry = orient(polygon=geometry)
        self.diameter = diameter
        self.distance = distance
        self.material = material
        self.shear_check = shear_check
        self.torsion_check = torsion_check
        self.anchorage_length = anchorage_length
        self._mandrel_diameter_factor = mandrel_diameter_factor
        self.based_on_cover = based_on_cover
        self._id = StirrupConfiguration.counter
        self._validation_relative_position(relative_position=relative_start_position)
        self._validation_relative_position(relative_position=relative_end_position)
        self._relative_start_position = relative_start_position
        self._relative_end_position = relative_end_position
        self.n_vertices_used = n_vertices_used
        self._cover_used = cover_used
        self._amount_of_legs = 2
        StirrupConfiguration.counter += 1

    @property
    def mandrel_diameter_factor(self) -> DIMENSIONLESS:
        """Diameter factor of mandrel.
        Standard values given by Dutch Annex Table 8.1Na - NEN-EN 1992-1-1+C2:2011/NB+A1:2020
        (default: 4⌀ for ⌀<=16mm and 5⌀ for ⌀>16mm).
        """
        if self._mandrel_diameter_factor:
            return self._mandrel_diameter_factor
        return 5.0 if self.diameter > 16.0 else 4.0

    @property
    def as_w(self) -> MM2_M:
        """Total cross-sectional area of the stirrup [mm²/m]."""
        return self._amount_of_legs * self.area * (M_TO_MM / self.distance)

    @property
    def area(self) -> MM2:
        """Area of the stirrup bar [mm²]."""
        return 0.25 * np.pi * self.diameter**2

    @property
    def radius(self) -> MM:
        """Radius of the stirrup bar [mm]."""
        return self.diameter / 2

    @property
    def centroid(self) -> Point:
        """Centroid of the stirrup bar [mm]."""
        return self.geometry.centroid

    @property
    def weight_per_meter(self) -> KG_M3:
        """Total mass of the stirrup per meter length in the longitudinal direction (concrete+reinforcement) [kg/m³]
        (Weight of a single stirrup x amount of stirrups present in one meter length).
        """
        return self.material.density * self.geometry.length * self.area * MM3_TO_M3 * M_TO_MM / self.distance

    @property
    def ctc_distance_legs(self) -> MM:
        """Distance between the legs of the stirrup taken form the center lines of the rebar [mm]."""
        min_x, max_x = self.geometry.bounds[0], self.geometry.bounds[2]
        return max_x - min_x

    @property
    def cover_used(self) -> float:
        """Can be used to store the value of the cover used when adding the stirrup to the cross-section [mm]."""
        return self._cover_used or 0.0

    @property
    def relative_start_position(self) -> RATIO:
        """Relative position of the start of the stirrup configuration inside the cross-section. Value between 0 and 1."""
        return self._relative_start_position

    @property
    def relative_end_position(self) -> RATIO:
        """Relative position of the end of the stirrup configuration inside the cross-section. Value between 0 and 1."""
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

    def __str__(self) -> str:
        """String representation of the stirrup."""
        return f"Stirrups ⌀{self.diameter}-{self.distance:.0f} mm | {self.material.name} | {self.as_w:.2f} mm²/m"
