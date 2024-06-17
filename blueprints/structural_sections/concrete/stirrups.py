"""Stirrups module."""

import numpy as np
from shapely import Point, Polygon

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MM2, MM2_M
from blueprints.unit_conversion import M_TO_MM, MM3_TO_M3


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


STIRRUP_COLOR = (0.412, 0.412, 0.412)
