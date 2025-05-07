"""Module containing the class definition for a steel cross-section element."""

from dataclasses import dataclass

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import KG_M, MM, MPA
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class SteelElement:
    """
    General class for a steel cross-section element.

    Parameters
    ----------
    cross_section : CrossSection
        The cross-section of the steel element.
    material : SteelMaterial
        The material of the steel element.
    nominal_thickness : MM
        The nominal thickness of the steel element.

        This is used to calculate the yield and ultimate strength of the steel element.
        But be aware that there is no internal check to make sure that the given nominal thickness of this steel element
        is actually the same thickness of the cross-section.
    """

    cross_section: CrossSection
    material: SteelMaterial
    nominal_thickness: MM

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
        fy = self.material.yield_strength(thickness=self.nominal_thickness)
        if fy is None:
            raise ValueError("Yield strength is not defined for this material.")
        return fy

    @property
    def ultimate_strength(self) -> MPA:
        """
        Calculate the ultimate strength of the steel element.

        Returns
        -------
        MPa
            The ultimate strength of the steel element.
        """
        fu = self.material.ultimate_strength(thickness=self.nominal_thickness)
        if fu is None:
            raise ValueError("Ultimate strength is not defined for this material.")
        return fu
