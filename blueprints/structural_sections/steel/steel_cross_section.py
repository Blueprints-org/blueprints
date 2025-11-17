"""Module containing the class definition for a steel cross-section."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import DEG, KG_M, MM
from blueprints.unit_conversion import MM2_TO_M2


class SteelCrossSectionProtocol(Protocol):
    """Protocol for steel cross-sections."""

    @property
    def weight_per_meter(self) -> KG_M:
        """Weight per meter of the steel cross-section."""
        ...


@dataclass(frozen=True, kw_only=True)
class SteelCrossSection(SteelCrossSectionProtocol):
    """
    Representation of a steel cross-section for any given cross-section or profile.

    Parameters
    ----------
    cross_section : CrossSection
        The cross-section. This can be a predefined profile or a generic cross-section.
    material : SteelMaterial
        The material type of the steel.

    Notes
    -----
    The following parameters are only used for positioning and orienting the cross-section
    in the context of a combined cross-section. They can be set after instantiation using the
    `add_steel_cross_section` method of the `CombinedSteelCrossSection` class.
    x_offset : MM, optional
        The x-coordinate offset of the cross-section's centroid [mm]. Default is 0.0.
    y_offset : MM, optional
        The y-coordinate offset of the cross-section's centroid [mm]. Default is 0.0.
    rotation_angle : DEG, optional
        The rotation angle of the cross-section in degrees (counter-clockwise). Default is 0.0
    """

    cross_section: CrossSection
    """The cross-section. This can be a predefined profile or a generic cross-section."""
    material: SteelMaterial
    """The material type of the steel."""
    x_offset: MM = field(init=False, default=0.0)
    """The x-coordinate offset of the cross-section's centroid [mm]."""
    y_offset: MM = field(init=False, default=0.0)
    """The y-coordinate offset of the cross-section's centroid [mm]."""
    rotation_angle: DEG = field(init=False, default=0.0)
    """The rotation angle of the cross-section in degrees (counter-clockwise)."""

    @property
    def weight_per_meter(self) -> KG_M:
        """
        Calculate the weight per meter of the steel cross-section.

        Returns
        -------
        KG_M
            The weight per meter of the steel cross-section.
        """
        return self.material.density * (self.cross_section.area * MM2_TO_M2)

    def _transform(self, x_offset: MM, y_offset: MM, rotation_angle: DEG) -> SteelCrossSection:
        """
        Create a transformed steel cross-section.

        Parameters
        ----------
        x_offset : MM
            The x-coordinate offset of the cross-section's centroid [mm].
        y_offset : MM
            The y-coordinate offset of the cross-section's centroid [mm].
        rotation_angle : DEG
            The rotation angle of the cross-section in degrees (counter-clockwise).

        Returns
        -------
        SteelCrossSection
            The transformed steel cross-section.
        """
        transformed_section = SteelCrossSection(
            cross_section=self.cross_section,
            material=self.material,
        )
        object.__setattr__(transformed_section, "x_offset", x_offset)
        object.__setattr__(transformed_section, "y_offset", y_offset)
        object.__setattr__(transformed_section, "rotation_angle", rotation_angle)
        return transformed_section
