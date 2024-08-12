"""Rebar class for the representation of reinforcement bars in a cross-section."""

from dataclasses import dataclass

from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.cross_section_shapes import CircularCrossSection
from blueprints.type_alias import KG_M, RATIO
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class Rebar(CircularCrossSection):
    """
    Representation of a reinforcement bar from a cross-section perspective. For example ⌀16, ⌀20, ⌀25, ⌀32,etc.

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
        Relative position of the start of the rebar in the longitudinal direction of the host element [-]
    relative_end_position: RATIO
        Relative position of the end of the rebar in the longitudinal direction of the host element [-]
    """

    material: ReinforcementSteelMaterial
    relative_start_position: RATIO = 0.0
    relative_end_position: RATIO = 1.0

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameter."""
        super().__post_init__()
        if not 0.0 <= self.relative_end_position <= 1.0:
            msg = f"Relative end position of the rebar must be between 0.0 and 1.0, but got {self.relative_end_position}"
            raise ValueError(msg)

        if not 0.0 <= self.relative_start_position <= 1.0:
            msg = f"Relative start position of the rebar must be between 0.0 and 1.0, but got {self.relative_start_position}"
            raise ValueError(msg)

    @property
    def weight_per_meter(self) -> KG_M:
        """Unit weight of rebar per meter [kg/m].

        Returns
        -------
        float
            Example: 1.578336149163512 for ⌀16 and normal density of 7850 kg/m3
        """
        return self.material.density * (self.area * MM2_TO_M2)
