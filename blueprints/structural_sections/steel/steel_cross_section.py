"""Module containing the class definition for a steel cross-section."""

from __future__ import annotations

from dataclasses import dataclass

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import KG_M
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
    """

    cross_section: CrossSection
    """The cross-section. This can be a predefined profile or a generic cross-section."""
    material: SteelMaterial
    """The material type of the steel."""

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
