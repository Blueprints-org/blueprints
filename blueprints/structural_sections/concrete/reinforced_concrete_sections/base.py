"""Base class of all reinforced cross-sections."""

from abc import ABC
from collections.abc import Callable
from functools import partial

from shapely import LineString

from blueprints.materials.concrete import ConcreteMaterial
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import (
    ReinforcementConfiguration,
)
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration
from blueprints.structural_sections.cross_section_shapes import CrossSection
from blueprints.type_alias import KG_M, KG_M3, M3_M, MM2_M
from blueprints.unit_conversion import M_TO_MM, MM3_TO_M3


class ReinforcedCrossSection(ABC):
    """Base class of all reinforced cross-sections."""

    def __init__(
        self,
        cross_section: CrossSection,
        concrete_material: ConcreteMaterial,
    ) -> None:
        """Initialize the reinforced cross-section.

        Parameters
        ----------
        cross_section : CrossSection
            Cross-section of the reinforced concrete section.
        concrete_material : ConcreteMaterial
            Material properties of the concrete.
        """
        self.cross_section = cross_section
        self.concrete_material = concrete_material
        self._reinforcement_configurations: list[tuple[LineString | Callable[..., LineString], ReinforcementConfiguration]] = []
        self._single_longitudinal_rebars: list[Rebar] = []
        self._stirrups: list[StirrupConfiguration] = []

    @property
    def longitudinal_rebars(self) -> list[Rebar]:
        """Return a list of all longitudinal rebars."""
        rebars: list[Rebar] = []

        # add the single longitudinal rebars
        rebars.extend(self._single_longitudinal_rebars)

        # add the rebars from the reinforcement configurations
        for line, configuration in self._reinforcement_configurations:
            if callable(line):
                # partial function with additional arguments where the line should be called to get the LineString
                # the implementation will be made at that level and inserted here to produce the rebars needed.
                # this keeps this ABC class clean and allows for a lot of flexibility in the implementation of the line.
                # this has been done to be able to add any shape of line to the cross-section (e.g. a circle or any other in the future).
                rebars.extend(configuration.to_rebars(line=line()))
            else:
                rebars.extend(configuration.to_rebars(line=line))

        # check if all rebars are inside the cross-section.
        # needed for the case where custom configurations are added to the RCS
        for rebar in rebars:
            if not self.cross_section.geometry.contains(other=rebar.geometry):
                msg = f"Rebar (diameter={rebar.diameter}, x={rebar.x}, y={rebar.y}) is not (fully) inside the cross-section."
                raise ValueError(msg)

        return rebars

    @property
    def stirrups(self) -> list[StirrupConfiguration]:
        """Return a list of all stirrups."""
        return self._stirrups

    @property
    def reinforcement_weight_longitudinal_bars(self) -> KG_M:
        """Total mass of the longitudinal reinforcement in the cross-section per meter length [kg/m]."""
        return sum(rebar.weight_per_meter for rebar in self.longitudinal_rebars)

    @property
    def reinforcement_weight_stirrups(self) -> KG_M:
        """Total mass of the stirrups' reinforcement in the cross-section per meter length [kg/m]."""
        return sum(stirrup.weight_per_meter for stirrup in self._stirrups)

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

    def get_present_steel_materials(self) -> list[ReinforcementSteelMaterial]:
        """Return a list of all present steel materials in the cross-section."""
        materials = [rebar.material for rebar in self.longitudinal_rebars]
        materials.extend(stirrup.material for stirrup in self._stirrups)
        return list(set(materials))

    def add_longitudinal_rebar(
        self,
        rebar: Rebar,
    ) -> Rebar:
        """Adds a single reinforcement bar to the cross-section.

        Parameters
        ----------
        rebar : Rebar
            Rebar to be added to the cross-section.

        Raises
        ------
        ValueError
            If the rebar is not fully inside the cross-section.

        Returns
        -------
        Rebar
            Newly created Rebar
        """
        # check if given diameter/coordinates are fully inside the cross-section
        if not rebar.geometry.within(self.cross_section.geometry):
            msg = f"Rebar (diameter={rebar.diameter}, x={rebar.x}, y={rebar.y}) is not (fully) inside the cross-section."
            raise ValueError(msg)

        # add the rebar to the list of longitudinal rebars
        self._single_longitudinal_rebars.append(rebar)

        return rebar

    def add_stirrup_configuration(self, stirrup: StirrupConfiguration) -> StirrupConfiguration:
        """Add a stirrup configuration to the cross-section.

        Parameters
        ----------
        stirrup : StirrupConfiguration
            Configuration of stirrup reinforcement in the cross-section.

        Returns
        -------
        StirrupConfiguration
            Newly created Stirrup

        Raises
        ------
        ValueError
            If the stirrup is not fully inside the cross-section.
        """
        # check if the stirrup is inside the cross-section
        stirrup_outside_edge = stirrup.geometry.buffer(distance=stirrup.diameter / 2)
        if not self.cross_section.geometry.contains(stirrup_outside_edge):
            msg = "Stirrup is not (fully) inside the cross-section."
            raise ValueError(msg)

        # add the stirrup to the list
        self._stirrups.append(stirrup)

        return stirrup

    def add_reinforcement_configuration(
        self,
        line: LineString | Callable[..., LineString],
        configuration: ReinforcementConfiguration,
        *args,
        **kwargs,
    ) -> None:
        """Add a reinforcement configuration to the cross-section.

        Parameters
        ----------
        line : LineString | Callable[..., LineString]
            Representing the path of the reinforcement in the cross-section.
            Start of the line defines the first rebar of the configuration, end of the line defines the last rebar.
            If a callable is given, it should return a LineString. The callable can take additional arguments.
            Arguments can be passed to the callable using the *args and **kwargs.
        configuration : ReinforcementConfiguration
            Configuration of the reinforcement.
        args : Any
            Additional arguments for the callable line. If line is not a callable, these arguments are ignored.
        kwargs : Any
            Additional keyword arguments for the callable line. If line is not a callable, these arguments are ignored.

        """
        # check if the line is a callable and wrap it with the given arguments
        if callable(line):
            line = partial(line, *args, **kwargs)  # type: ignore[misc]

        # add the reinforcement configuration to the list
        self._reinforcement_configurations.append((line, configuration))
