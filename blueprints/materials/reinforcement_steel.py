"""Module for reinforcement steel material properties."""

from dataclasses import dataclass, field
from enum import Enum

from blueprints.materials.constants import STEEL_YOUNG_MODULUS
from blueprints.type_alias import DIMENSIONLESS, KG_M3, MPA, PER_MILLE


class ReinforcementType(Enum):
    """Enumeration of product form / reinforcement type."""

    BARS = "Bars"
    DECOILED_RODS = "Decoiled rods"
    WIRE_FABRICS = "Wire fabrics"
    LATTICE_GIRDERS = "Lattice girders"


class ReinforcementSteelQuality(Enum):
    """Enumeration of reinforcement steel quality."""

    B400A = "B400A"
    B500A = "B500A"
    B600A = "B600A"
    B400B = "B400B"
    B500B = "B500B"
    B600B = "B600B"
    B400C = "B400C"
    B500C = "B500C"
    B600C = "B600C"
    B550A = "B550A"
    B550B = "B550B"


class ReinforcementSteelClass(Enum):
    """Enumeration of reinforcement steel classes."""

    A = "A"
    B = "B"
    C = "C"


class ReinforcementBarSurface(Enum):
    """Enumeration of types of bar surface."""

    SMOOTH = "Smooth"
    RIBBED = "Ribbed"


class SteelFabrication(Enum):
    """Enumeration of types of fabrication."""

    HOT_ROLLED = "Hot-rolled"
    COLD_WORKED = "Cold-worked"


class ReinforcementDiagramType(Enum):
    """Enumeration of types of stress-strain diagrams."""

    BILINEAR_INCLINED = "Bi-linear with inclined branch"
    BILINEAR_NOT_INCLINED = "Bi-linear with horizontal branch"
    USER = "User-defined"


@dataclass(frozen=True)
class ReinforcementSteelMaterial:
    r"""Representation of the properties of reinforcement steel suitable for use with NEN-EN 1992-1-1.

    Based on the analytical relations shown on table C.1 Annex C.

    Parameters
    ----------
    steel_quality: ReinforcementSteelQuality,
        Steel quality of the ReinforcementSteelMaterial object (default: B500B).
    density: KG_M3
        Unit weight of steel [kg/m³] (default= 7850.0) [$kg/m^3$]
    reinforcement_type: ReinforcementType
        Product form / Reinforcement type (default=ReinforcementType.BARS)
    bar_surface: ReinforcementBarSurface
        Type of bar surface (default=ReinforcementBarSurface.RIBBED)
    steel_fabrication: SteelFabrication
        Type of fabrication (default=SteelFabrication.HOT_ROLLED)
    diagram_type: ReinforcementDiagramType
        Type of stress-strain diagram (default=ReinforcementDiagramType.BILINEAR_INCLINED)
    custom_name: str
        User-defined name of the material (default= name of steel quality; example: 'B500B')
    custom_e_s: MPA
        User-defined Young's modulus of the material, if not provided the default value is used (default=200000) [$MPa$]

    """

    steel_quality: ReinforcementSteelQuality = field(default=ReinforcementSteelQuality.B500B)
    density: KG_M3 = field(default=7850.0, metadata={"unit": "kg/m³"})
    reinforcement_type: ReinforcementType = field(default=ReinforcementType.BARS)
    bar_surface: ReinforcementBarSurface = field(default=ReinforcementBarSurface.RIBBED)
    steel_fabrication: SteelFabrication = field(default=SteelFabrication.HOT_ROLLED)
    diagram_type: ReinforcementDiagramType = field(default=ReinforcementDiagramType.BILINEAR_NOT_INCLINED)
    custom_name: str | None = field(default=None, compare=False)
    custom_e_s: MPA | None = field(default=None, metadata={"unit": "MPa"})

    @property
    def name(self) -> str:
        r"""Name of the reinforcement steel material.

        Returns
        -------
        str
            Example: "B500B"
        """
        if self.custom_name:
            return self.custom_name
        return self.steel_quality.value

    @property
    def e_s(self) -> MPA:
        r"""Reinforcement steel Young's modulus [$MPa$].

        Returns
        -------
        MPA
            Example: 200000.0 (for B500B)
        """
        if self.custom_e_s:
            return self.custom_e_s
        return STEEL_YOUNG_MODULUS

    @property
    def f_yk(self) -> MPA:
        r"""[$f_{yk}$] Characteristic yield strength of reinforcement [$MPa$].

        Returns
        -------
        MPA
            Example: 500.0 (for B500B)
        """
        return float(self.steel_quality.value[1:-1])

    @property
    def steel_class(self) -> str:
        r"""Reinforcement class.

        Returns
        -------
        str
            Example: "B" (for B500B)
        """
        return self.steel_quality.value[-1]

    @property
    def f_tk(self) -> MPA:
        r"""[$f_{tk}$] Characteristic tensile strength of reinforcement [$MPa$].

        Returns
        -------
        MPA
            Example: 540.0 (for B500B)
        """
        return self.f_yk * self.ductility_factor_k

    @property
    def ductility_factor_k(self) -> DIMENSIONLESS:
        r"""Ductility factor k [$-$] -> ([$f_{tk}$] / [$f_{yk}$]) tabel C.1 Annex C from NEN-EN 1992-1-1.

        * 1.05 for steel class A
        * 1.08 for steel class B
        * 1.15 for steel class C

        Returns
        -------
        DIMENSIONLESS
            Example: 1.08 (for B500B)
        """
        match self.steel_class.lower():
            case "a":
                return 1.05
            case "b":
                return 1.08
            case "c":
                return 1.15
            case _:
                raise ValueError(f"Unknown steel class: {self.steel_class}")

    @property
    def eps_uk(self) -> PER_MILLE:
        r"""[$\varepsilon_{uk}$] Characteristic strain of reinforcement at max. load [$‰$ (per mille)] (tabel C.1 Annex C from NEN-EN 1992-1-1).

        * 250 ‰ for steel class A
        * 500 ‰ for steel class B
        * 750 ‰ for steel class C

        Returns
        -------
        PER_MILLE
            Example: 500 (for B500B)
        """
        match self.steel_class.lower():
            case "a":
                return 250
            case "b":
                return 500
            case "c":
                return 750
            case _:
                raise ValueError(f"Unknown steel class: {self.steel_class}")
