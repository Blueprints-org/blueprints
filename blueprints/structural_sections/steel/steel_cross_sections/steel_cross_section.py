"""Module containing the class definition for a steel cross-section element."""

from dataclasses import dataclass

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import KG_M, MM, MPA
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class SteelCrossSection:
    """
    Representation of steel cross-sections for any given cross-section.

    Parameters
    ----------
    cross_section : CrossSection
        The cross-section.
    material : SteelMaterial
        The material type of the steel.
    """

    cross_section: CrossSection
    material: SteelMaterial

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

    def yield_strength(self, nominal_thickness: MM) -> MPA:
        """
        Calculate the yield strength of the steel element.

        Parameters
        ----------
        nominal_thickness : MM
            The nominal thickness of the steel cross-section.

        Attention: There is no internal check to make sure that the given nominal thickness of this steel cross-section
        is actually the same thickness of the cross-section.

        Returns
        -------
        MPa
            The yield strength of the steel element.
        """
        fy = self.material.yield_strength(thickness=nominal_thickness)
        if fy is None:
            raise ValueError("Yield strength is not defined for this material.")
        return fy

    def ultimate_strength(self, nominal_thickness: MM) -> MPA:
        """
        Calculate the ultimate strength of the steel element.

        Parameters
        ----------
        nominal_thickness : MM
            The nominal thickness of the steel cross-section.

        Attention: There is no internal check to make sure that the given nominal thickness of this steel cross-section
        is actually the same thickness of the cross-section.

        Returns
        -------
        MPa
            The ultimate strength of the steel element.
        """
        fu = self.material.ultimate_strength(thickness=nominal_thickness)
        if fu is None:
            raise ValueError("Ultimate strength is not defined for this material.")
        return fu
