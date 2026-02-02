"""Module containing the class definition for a steel cross-section."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.standard_profiles import HEA, HEB, HEM, IPE, RHS, RHSCF, SHS, SHSCF
from blueprints.type_alias import KG_M, MPA
from blueprints.unit_conversion import MM2_TO_M2


class FabricationMethod(StrEnum):
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
        """Set fabrication method if not provided based on standard profiles."""
        if self.fabrication_method is None and hasattr(self.profile, "name"):
            self._set_fabrication_method()

    def _set_fabrication_method(self) -> None:
        """
        Determines and sets the fabrication method based on the profile name and geometry.
        IPE, RHS, SHS, HEB, HEA, HEM are hot-rolled. RHSCF, SHSCF are cold-formed.

        Returns
        -------
        None
        """
        profile_name, corrosion, corrosion_inside, corrosion_outside = self._get_profile_name_and_corrosion_amount(self.profile.name)
        hot_rolled_profiles = [(cls, "_database") for cls in (IPE, RHS, SHS, HEB, HEA, HEM)]
        cold_formed_profiles = [(cls, "_database") for cls in (RHSCF, SHSCF)]
        if self._set_fabrication_if_in_db(
            profile_name, corrosion, corrosion_inside, corrosion_outside, hot_rolled_profiles, FabricationMethod.HOT_ROLLED
        ):
            return
        self._set_fabrication_if_in_db(
            profile_name, corrosion, corrosion_inside, corrosion_outside, cold_formed_profiles, FabricationMethod.COLD_FORMED
        )

    @staticmethod
    def _get_profile_name_and_corrosion_amount(full_name: str) -> tuple[str, float | None, float | None, float | None]:
        """Extracts the profile name and corrosion amounts from the full profile name.
        Single corrosion format: "ProfileName (corrosion: X mm)".
        Double corrosion format: "ProfileName (corrosion inside: X mm, outside: Y mm)".

        Parameters
        ----------
        full_name : str
            The full profile name possibly containing corrosion information.

        Returns
        -------
        tuple[str, float | None, float | None, float | None]
            A tuple containing the profile name, single corrosion amount, inside corrosion amount, and outside corrosion amount.
        """
        # Single corrosion: (corrosion: X mm)
        single = re.match(r"^(.*?)\s*\(corrosion:\s*([0-9.]+)\s*mm\)\s*$", full_name)
        if single:
            return single.group(1).strip().replace(".", "_"), float(single.group(2)), None, None
        # Double corrosion: (corrosion inside: X mm, outside: Y mm)
        double = re.match(r"^(.*?)\s*\(corrosion\s+inside:\s*([0-9.]+)\s*mm,\s*outside:\s*([0-9.]+)\s*mm\)\s*$", full_name)
        if double:
            return double.group(1).strip().replace(".", "_"), None, float(double.group(2)), float(double.group(3))
        return full_name.strip().replace(".", "_"), None, None, None

    def _set_fabrication_if_in_db(
        self,
        profile_name: str,
        corrosion: float | None,
        corrosion_inside: float | None,
        corrosion_outside: float | None,
        profile_classes: list[tuple[type, str]],
        fabrication_method: FabricationMethod,
    ) -> bool:
        for profile_class, db_attr in profile_classes:
            if hasattr(profile_class, db_attr) and hasattr(profile_class, "_factory"):
                db = getattr(profile_class, db_attr)
                factory = getattr(profile_class, "_factory")
                if profile_name in db:
                    db_params = db[profile_name]
                    db_kwargs = {field: getattr(db_params, field) for field in db_params._fields}
                    db_profile = factory(**db_kwargs)
                    if corrosion is not None and hasattr(db_profile, "with_corrosion"):
                        db_profile = db_profile.with_corrosion(corrosion=corrosion)
                    elif (corrosion_inside is not None or corrosion_outside is not None) and hasattr(db_profile, "with_corrosion"):
                        db_profile = db_profile.with_corrosion(corrosion_inside=corrosion_inside, corrosion_outside=corrosion_outside)
                    if hasattr(self.profile, "polygon") and hasattr(db_profile, "polygon") and self.profile.polygon.equals(db_profile.polygon):
                        object.__setattr__(self, "fabrication_method", fabrication_method)
                        return True
        return False

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
