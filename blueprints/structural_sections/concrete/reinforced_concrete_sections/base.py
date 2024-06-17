"""Base class of all reinforced cross-sections."""

# ruff: noqa: TRY004
from abc import ABC, abstractmethod

from matplotlib import pyplot as plt
from plotly import graph_objects as go
from shapely import Point

from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_sections_shapes import CrossSection, Edges
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import (
    ReinforcementByDistance,
    ReinforcementByQuantity,
    ReinforcementInLine,
)
from blueprints.structural_sections.concrete.stirrups import Stirrup
from blueprints.type_alias import DIMENSIONLESS, KG_M, KG_M3, M3_M, MM, MM2_M
from blueprints.unit_conversion import M_TO_MM, MM3_TO_M3


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
