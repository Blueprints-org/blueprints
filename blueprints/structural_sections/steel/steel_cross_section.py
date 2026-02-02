"""Module containing the class definition for a steel cross-section."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.standard_profiles import HEA, HEB, HEM, IPE, RHS, RHSCF, SHS, SHSCF
from blueprints.type_alias import KG_M, MPA
from blueprints.unit_conversion import MM2_TO_M2


class FabricationMethod(Enum):
    """Enumeration of steel cross-section fabrication methods."""

    COLD_FORMED = "cold-formed"
    HOT_ROLLED = "hot-rolled"
    WELDED = "welded"


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
    fabrication_method : Optional[FabricationMethod]
        The fabrication method of the steel cross-section, either FabricationMethod.COLD_FORMED,
        FabricationMethod.HOT_ROLLED, or FabricationMethod.WELDED. Default is None.
    """

    profile: Profile
    """The profile. This can be a predefined profile or a generic profile."""
    material: SteelMaterial
    """The material type of the steel."""
    fabrication_method: FabricationMethod | None = None
    """The fabrication method of the steel cross-section, either FabricationMethod.COLD_FORMED,
    FabricationMethod.HOT_ROLLED, or FabricationMethod.WELDED. Default is None."""

    def __post_init__(self) -> None:
        """
        Set fabrication method if not provided based on standard profiles.
        IPE, RHS, SHS, HEB, HEA, HEM are hot-rolled.
        RHSCF, SHSCF are cold-formed.
        Filters database names: strips whitespace and removes anything in parentheses before matching.
        """

        def clean_name(name: str) -> str:
            # Remove anything in parentheses and strip whitespace
            name = re.sub(r"\(.*?\)", "", name)
            return name.strip()

        if self.fabrication_method is None and hasattr(self.profile, "name"):
            profile_name = clean_name(self.profile.name)
            standard_profiles_hot_rolled = [
                (IPE, "_database"),
                (RHS, "_database"),
                (SHS, "_database"),
                (HEB, "_database"),
                (HEA, "_database"),
                (HEM, "_database"),
            ]
            for profile_class, db_attr in standard_profiles_hot_rolled:
                if hasattr(profile_class, db_attr):
                    db = getattr(profile_class, db_attr)
                    db_names = {clean_name(n) for n in db}
                    if profile_name in db_names:
                        object.__setattr__(self, "fabrication_method", FabricationMethod.HOT_ROLLED)
                        break
            standard_profiles_cold_formed = [
                (RHSCF, "_database"),
                (SHSCF, "_database"),
            ]
            for profile_class, db_attr in standard_profiles_cold_formed:
                if hasattr(profile_class, db_attr):
                    db = getattr(profile_class, db_attr)
                    db_names = {clean_name(n) for n in db}
                    if profile_name in db_names:
                        object.__setattr__(self, "fabrication_method", FabricationMethod.COLD_FORMED)
                        break

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
