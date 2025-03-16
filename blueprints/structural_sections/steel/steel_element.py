"""Module containing the class definition for a steel cross-section element."""

from dataclasses import dataclass

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.general_cross_section import CrossSection
from blueprints.type_alias import KG_M, MPA
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class SteelElement:
    """
    General class for a steel cross-section element.

    Parameters
    ----------
    material : SteelMaterial
        The material properties of the steel element.
    cross_section : CrossSection
        The cross-section of the steel element.
    """

    material: SteelMaterial
    cross_section: CrossSection

    def __post_init__(self) -> None:
        """Post-initialization to validate the material."""
        if self.material is None:
            raise ValueError("Material of the steel element cannot be None.")

    @property
    def weight_per_meter(self) -> KG_M:
        """
        Calculate the weight per meter of the steel element.

        Returns
        -------
        KG_M
            The weight per meter of the steel element.
        """
        return self.material.density * (self.cross_section.area * MM2_TO_M2)

    @property
    def yield_strength(self) -> MPA:
        """
        Calculate the yield strength of the steel element.

        Returns
        -------
        MPa
            The yield strength of the steel element.
        """
        return self.material.yield_strength()

    @property
    def ultimate_strength(self) -> MPA:
        """
        Calculate the ultimate strength of the steel element.

        Returns
        -------
        MPa
            The ultimate strength of the steel element.
        """
        return self.material.ultimate_strength()
