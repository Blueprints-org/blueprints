"""Module for bolt material properties.

The bolt classes and their nominal strengths come from Table 3.1 of EN 1993-1-8:2005; that table is
implemented in the codes tree and is imported here, the same way SteelMaterial reads its strengths
from Table 3.1 of EN 1993-1-1:2005. BoltClass is re-exported from this module so that callers can
reach the classification and the material through one import.

The thread dimensions are not part of any Eurocode. They come from the ISO metric coarse thread
series and are held here because the resistance formulas of EN 1993-1-8 consume them directly.

Not implemented, and deliberately left open for extension: the preload force and the slip resistance
of art.3.9, which are properties of the connection rather than of the bolt, and injection bolts of
art.3.6.2, which carry their own resistance rules.
"""

import math
from dataclasses import dataclass, field
from enum import StrEnum

from blueprints.codes.eurocode.en_1993_1_8_2005.chapter_3_connections_made_with_bolts_rivets_or_pins.table_3_1 import (
    BoltClass,
    Table3Dot1NominalValuesBolts,
)
from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MM2, MPA, PER_DEGREE

__all__ = ["BoltClass", "BoltMaterial", "BoltSize"]

# default data from EN 1993-1-1:2005 art.3.2.6
BOLT_YOUNG_MODULUS = 210_000.0  # [MPa]
BOLT_POISSON_RATIO = 0.3  # [-]
BOLT_THERMAL_COEFFICIENT = 1.2e-5  # [1/°C]


class BoltSize(StrEnum):
    """Bolt sizes of the ISO metric coarse thread series.

    The nominal diameter and the tensile stress area are properties of the thread, not of any
    Eurocode. They are held here because the resistance formulas of EN 1993-1-8 take them as input:
    the tensile stress area where the shear plane passes through the threads, and the gross area
    where it passes through the shank.
    """

    M8 = "M8"
    M10 = "M10"
    M12 = "M12"
    M14 = "M14"
    M16 = "M16"
    M18 = "M18"
    M20 = "M20"
    M22 = "M22"
    M24 = "M24"
    M27 = "M27"
    M30 = "M30"
    M33 = "M33"
    M36 = "M36"

    @property
    def diameter(self) -> MM:
        """[$d$] Nominal diameter of the bolt [$mm$].

        Returns
        -------
        MM
            The number of the designation, so 20 mm for M20.
        """
        return float(self.value.removeprefix("M"))

    @property
    def gross_area(self) -> MM2:
        """[$A$] Gross cross-section of the bolt shank [$mm^2$].

        Returns
        -------
        MM2
            The area of a circle of the nominal diameter, which is the area to use where the shear
            plane passes through the unthreaded shank.
        """
        return math.pi * self.diameter**2 / 4

    @property
    def tensile_stress_area(self) -> MM2:
        """[$A_s$] Tensile stress area of the bolt [$mm^2$].

        Returns
        -------
        MM2
            The tensile stress area of the ISO metric coarse thread, which is the area to use for the
            tension resistance and where the shear plane passes through the threaded portion.
        """
        return _TENSILE_STRESS_AREA[self]


# Tensile stress area of the ISO metric coarse thread series [mm2]
_TENSILE_STRESS_AREA: dict[BoltSize, MM2] = {
    BoltSize.M8: 36.6,
    BoltSize.M10: 58.0,
    BoltSize.M12: 84.3,
    BoltSize.M14: 115.0,
    BoltSize.M16: 157.0,
    BoltSize.M18: 192.0,
    BoltSize.M20: 245.0,
    BoltSize.M22: 303.0,
    BoltSize.M24: 353.0,
    BoltSize.M27: 459.0,
    BoltSize.M30: 561.0,
    BoltSize.M33: 694.0,
    BoltSize.M36: 817.0,
}


@dataclass(frozen=True)
class BoltMaterial:
    r"""Representation of the strength and deformation characteristics of a bolt.

    The strengths come from Table 3.1 of EN 1993-1-8:2005 unless a custom value is given. A custom
    strength takes the material outside the classes of that standard, so its rules no longer follow
    from the class; that is the caller's responsibility.

    Every numeric override is applied whenever it is not None, so a deliberate zero is honoured
    rather than silently replaced by the default. A zero thermal coefficient is the case that matters
    in practice, since it is how an analysis suppresses thermal expansion.

    Parameters
    ----------
    bolt_class : BoltClass
        Bolt class according to art.3.1.1(2) (default: 8.8).
    density : KG_M3
        Unit mass of the bolt [$kg/m^3$] (default: 7850.0).
    custom_name : str
        Use a custom name for the bolt material (default: the class designation).
    custom_e_modulus : MPA
        Use a custom modulus of elasticity [$MPa$] (default: 210000.0).
    custom_poisson_ratio : DIMENSIONLESS
        Use a custom Poisson's ratio (default: 0.3).
    custom_thermal_coefficient : PER_DEGREE
        Use a custom thermal coefficient (default: 1.2e-5).
    custom_yield_strength : MPA
        Use a custom yield strength [$f_{yb}$], which takes the bolt outside the classes of Table 3.1.
    custom_ultimate_strength : MPA
        Use a custom ultimate strength [$f_{ub}$], which takes the bolt outside the classes of
        Table 3.1.
    """

    bolt_class: BoltClass = field(default=BoltClass.CLASS_8_8)
    density: KG_M3 = field(default=7850.0, metadata={"unit": "kg/m³"})
    custom_name: str | None = field(default=None, compare=False)
    custom_e_modulus: MPA | None = field(default=None, metadata={"unit": "MPa"})
    custom_poisson_ratio: DIMENSIONLESS | None = field(default=None)
    custom_thermal_coefficient: PER_DEGREE | None = field(default=None)
    custom_yield_strength: MPA | None = field(default=None, metadata={"unit": "MPa"})
    custom_ultimate_strength: MPA | None = field(default=None, metadata={"unit": "MPa"})

    @property
    def name(self) -> str:
        """Name of the bolt material.

        Returns
        -------
        str
            Example: "8.8"
        """
        # Truthiness on purpose here, unlike the numeric overrides: an empty string is not a name, so
        # falling back to the class designation is more useful than returning it.
        if self.custom_name:
            return self.custom_name
        return self.bolt_class.value

    @property
    def e_modulus(self) -> MPA:
        """Modulus of elasticity of the bolt material.

        Returns
        -------
        MPA
            Modulus of elasticity [$MPa$].
        """
        if self.custom_e_modulus is not None:
            return self.custom_e_modulus
        return BOLT_YOUNG_MODULUS

    @property
    def poisson_ratio(self) -> DIMENSIONLESS:
        """Poisson's ratio of the bolt material.

        Returns
        -------
        DIMENSIONLESS
            Poisson's ratio of the material.
        """
        if self.custom_poisson_ratio is not None:
            return self.custom_poisson_ratio
        return BOLT_POISSON_RATIO

    @property
    def thermal_coefficient(self) -> PER_DEGREE:
        """Thermal coefficient of the bolt material [1/°C].

        Returns
        -------
        PER_DEGREE
            Thermal coefficient of the material.
        """
        if self.custom_thermal_coefficient is not None:
            return self.custom_thermal_coefficient
        return BOLT_THERMAL_COEFFICIENT

    @property
    def shear_modulus(self) -> MPA:
        """Shear modulus of the bolt material.

        Returns
        -------
        MPA
            Shear modulus of the material.
        """
        return self.e_modulus / (2 * (1 + self.poisson_ratio))

    @property
    def yield_strength(self) -> MPA:
        """[$f_{yb}$] Nominal yield strength of the bolt.

        Returns
        -------
        MPA
            The custom value where one is given, otherwise the value of Table 3.1 [$MPa$].
        """
        if self.custom_yield_strength is not None:
            return self.custom_yield_strength
        return Table3Dot1NominalValuesBolts(bolt_class=self.bolt_class).f_yb

    @property
    def ultimate_strength(self) -> MPA:
        """[$f_{ub}$] Nominal ultimate tensile strength of the bolt.

        Returns
        -------
        MPA
            The custom value where one is given, otherwise the value of Table 3.1 [$MPa$].
        """
        if self.custom_ultimate_strength is not None:
            return self.custom_ultimate_strength
        return Table3Dot1NominalValuesBolts(bolt_class=self.bolt_class).f_ub

    @property
    def can_be_preloaded(self) -> bool:
        """Whether the bolt may be used as a preloaded bolt.

        Art.3.1.2(1) allows only classes 8.8 and 10.9. A custom strength does not change the class, so
        this stays a property of the class. The preload force itself and the slip resistance of
        art.3.9 are properties of the connection and are not implemented here.

        Returns
        -------
        bool
            True for classes 8.8 and 10.9, False for the remaining classes.
        """
        return self.bolt_class.can_be_preloaded
