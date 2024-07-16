"""Rebar class for the representation of reinforcement bars in a cross-section."""

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_section_shapes import CircularCrossSection
from blueprints.type_alias import KG_M, MM, RATIO
from blueprints.unit_conversion import MM2_TO_M2


class Rebar(CircularCrossSection):
    """Representation of a reinforcement bar from a cross-section perspective. For example ⌀16, ⌀20, ⌀25, ⌀32,etc.

    Parameters
    ----------
    diameter : MM
        Diameter of the bar (for example: ⌀12, ⌀16, ⌀20, etc.) [mm]
    x : MM
        x-coordinate in the cross-section [mm]
    y : MM
        y-coordinate in the cross-section [mm]
    material : ReinforcementSteelMaterial
        Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.
    relative_start_position: RATIO
        Relative position of the start of the rebar in the longitudinal direction of the host cross-section [-]
    relative_end_position: RATIO
        Relative position of the end of the rebar in the longitudinal direction of the host cross-section [-]
    """

    def __init__(
        self,
        diameter: MM,
        x: MM,
        y: MM,
        material: ReinforcementSteelMaterial,
        relative_start_position: RATIO = 0.0,
        relative_end_position: RATIO = 1.0,
    ) -> None:
        """Initialize the Rebar object."""
        super().__init__(radius=diameter / 2, x=x, y=y)
        self.diameter = diameter
        self.x = x
        self.y = y
        self.material = material
        self.relative_start_position = relative_start_position
        self.relative_end_position = relative_end_position

    @property
    def diameter(self) -> MM:
        """Diameter of the rebar [mm]."""
        return self._diameter

    @diameter.setter
    def diameter(self, value: MM) -> None:
        """Set the diameter of the rebar."""
        if value <= 0.0:
            msg = "The diameter of the rebar must be greater than zero"
            raise ValueError(msg)
        self._diameter = value

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
    def relative_start_position(self) -> RATIO:
        """Relative position of the start of the rebar in the longitudinal direction of the host cross-section."""
        return self._relative_start_position

    @relative_start_position.setter
    def relative_start_position(self, value: RATIO) -> None:
        """Set the relative start position."""
        if not 0.0 <= value <= 1.0:
            msg = f"Relative start position of the rebar must be between 0.0 and 1.0, but got {value}"
            raise ValueError(msg)
        self._relative_start_position = value

    @property
    def relative_end_position(self) -> RATIO:
        """Relative position of the end of the rebar. In the longitudinal direction of the host cross-section."""
        return self._relative_end_position

    @relative_end_position.setter
    def relative_end_position(self, value: RATIO) -> None:
        """Set the relative end position."""
        if not 0.0 <= value <= 1.0:
            msg = f"Relative start position of the rebar must be between 0.0 and 1.0, but got {value}"
            raise ValueError(msg)
        self._relative_end_position = value
