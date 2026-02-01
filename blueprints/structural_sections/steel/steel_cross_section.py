"""Module containing the class definition for a steel cross-section."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import KG_M, MPA
from blueprints.unit_conversion import MM2_TO_M2


@dataclass(frozen=True, kw_only=True)
class SteelCrossSection:
    """
    Representation of a steel cross-section for any given profile and material.

    Parameters
    ----------
    profile : Profile
        The profile. This can be a predefined profile or a generic profile.
    material : SteelMaterial
        The material type of the steel.
    fabrication_method : Literal["rolled", "welded"], optional
        The fabrication method of the steel cross-section, either "rolled" or "welded. Default is "rolled".
    """

    profile: Profile
    """The profile. This can be a predefined profile or a generic profile."""
    material: SteelMaterial
    """The material type of the steel."""
    fabrication_method: Literal["rolled", "welded"] = "rolled"
    """The fabrication method of the steel cross-section, either "rolled" or "welded. Default is "rolled"."""

    @property
    def yield_strength(self) -> MPA:
        """
        Get the yield strength of the steel material.

        Returns
        -------
        MPA
            The yield strength of the steel material.
        """
        fy = self.material.yield_strength(thickness=self.profile.max_profile_thickness)
        return fy if fy is not None else 0

    @property
    def ultimate_strength(self) -> MPA:
        """
        Get the ultimate strength of the steel material.

        Returns
        -------
        MPA
            The ultimate strength of the steel material.
        """
        fu = self.material.ultimate_strength(thickness=self.profile.max_profile_thickness)
        return fu if fu is not None else 0

    @property
    def weight_per_meter(self) -> KG_M:
        """
        Calculate the weight per meter of the steel cross-section.

        Returns
        -------
        KG_M
            The weight per meter of the steel cross-section.
        """
        return self.material.density * (self.profile.area * MM2_TO_M2)
