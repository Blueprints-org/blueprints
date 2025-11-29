"""Module containing the class definition for a steel cross-section."""

from __future__ import annotations

from dataclasses import dataclass

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import DEG, KG_M, MM
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class SteelCrossSection:
    """
    Representation of a steel cross-section for any given cross-section or profile.

    Parameters
    ----------
    cross_section : CrossSection
        The cross-section. This can be a predefined profile or a generic cross-section.
    material : SteelMaterial
        The material type of the steel.
    horizontal_offset : MM, optional
        The horizontal offset of the cross-section's centroid [mm]. Default is 0.0.
    vertical_offset : MM, optional
        The vertical offset of the cross-section's centroid [mm]. Default is 0.0.
    rotation_angle : DEG, optional
        The rotation angle of the cross-section in degrees (counter-clockwise). Default is 0.0.
    """

    cross_section: CrossSection
    """The cross-section. This can be a predefined profile or a generic cross-section."""
    material: SteelMaterial
    """The material type of the steel."""
    horizontal_offset: MM = 0.0
    """The horizontal offset of the cross-section's centroid [mm]."""
    vertical_offset: MM = 0.0
    """The vertical offset of the cross-section's centroid [mm]."""
    rotation_angle: DEG = 0.0
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

    def transform(self, horizontal_offset: MM = 0.0, vertical_offset: MM = 0.0, rotation_angle: DEG = 0.0) -> SteelCrossSection:
        """
        Create a transformed steel cross-section.

        Parameters
        ----------
        horizontal_offset : MM, optional
            The horizontal offset of the cross-section's centroid [mm]. Default is 0.0.
        vertical_offset : MM, optional
            The vertical offset of the cross-section's centroid [mm]. Default is 0.0.
        rotation_angle : DEG, optional
            The rotation angle of the cross-section in degrees (counter-clockwise). Default is 0.0.

        Returns
        -------
        SteelCrossSection
            The transformed steel cross-section.
        """
        return SteelCrossSection(
            cross_section=self.cross_section,
            material=self.material,
            horizontal_offset=self.horizontal_offset + horizontal_offset,
            vertical_offset=self.vertical_offset + vertical_offset,
            rotation_angle=self.rotation_angle + rotation_angle,
        )
