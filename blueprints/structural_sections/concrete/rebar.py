"""Rebar class for the representation of reinforcement bars in a cross-section."""

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_sections_shapes import CircularCrossSection
from blueprints.type_alias import DIMENSIONLESS, KG_M, MM
from blueprints.unit_conversion import MM2_TO_M2

REBAR_COLOR = (0.50, 0, 0)


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
        self._set_diameter(diameter)
        self.x = x
        self.y = y
        self.material = material
        self._set_relative_start_position(relative_start_position)
        self._set_relative_end_position(relative_end_position)
        self.name = name if name else f"⌀{self.diameter}mm/{self.material.steel_quality.value}"

    def _set_diameter(self, value: MM) -> None:
        """Private method to set the diameter."""
        if value <= 0.0:
            raise ValueError("The diameter of the rebar must be greater than zero")
        self._diameter = value

    def _set_relative_start_position(self, value: DIMENSIONLESS) -> None:
        """Private method to set the relative start position."""
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Relative start position of the rebar must be between 0.0 and 1.0, but got {value}")
        self._relative_start_position = value

    def _set_relative_end_position(self, value: DIMENSIONLESS) -> None:
        """Private method to set the relative end position."""
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"Relative end position of the rebar must be between 0.0 and 1.0, but got {value}")
        self._relative_end_position = value

    @property
    def diameter(self) -> MM:
        """Diameter of the rebar [mm]."""
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
        return self._relative_start_position

    @property
    def relative_end_position(self) -> DIMENSIONLESS:
        """Relative position of the end of the rebar."""
        return self._relative_end_position
