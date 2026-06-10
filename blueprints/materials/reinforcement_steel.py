"""Module for reinforcement steel material properties."""

from dataclasses import dataclass, field
from enum import Enum

from blueprints.type_alias import DIMENSIONLESS, KG_M3, MPA, PER_MILLE, RATIO

REBAR_STEEL_YOUNG_MODULUS = 200_000.0  # [MPa] from EN 1992-1-1 3.2.7(4)


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
    r"""Representation of the properties of reinforcement steel suitable for use with EN 1992-1-1:2004.

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
    material_factor: DIMENSIONLESS
        Partial safety factor [$\gamma_s$] for reinforcement steel according to EN 1992-1-1 art.2.4.2.4 (1) - Table 2.1N [$-$] (default= 1.15)
        Persistent and transient        $\gamma_s = 1.15$
        Accidental design situations    $\gamma_s = 1.0$
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
    material_factor: DIMENSIONLESS = field(default=1.15)
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
        return REBAR_STEEL_YOUNG_MODULUS

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
    def f_yd(self) -> MPA:
        r"""[$f_{yd}$] Design yield strength of reinforcement (EN 1992-1-1:2004 art.3.2.7 (2)) [$MPa$].

        Returns
        -------
        MPA
            Example: 434.78 (for B500B)
        """
        return self.f_yk / self.material_factor

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
        r"""Ductility factor k [$-$] -> ([$f_{tk}$] / [$f_{yk}$]) table C.1 Annex C from EN 1992-1-1:2004.

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
        r"""[$\varepsilon_{uk}$] Characteristic strain of reinforcement at max. load [$‰$ (per mille)] (table C.1 Annex C from EN 1992-1-1:2004).

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


@dataclass(frozen=True)
class ReinforcementSteel:
    r"""Code-agnostic data container for the properties of reinforcement steel.

    All characteristic values are stored as plain data, so non-standard reinforcement can be created
    directly through the constructor without any design-code dependency. Use :meth:`from_ec2` to build
    an instance from an EN 1992-1-1 steel quality (Table C.1, Annex C). Only trivial derivations of
    stored fields are exposed as computed properties.

    Parameters
    ----------
    name: str
        Name of the reinforcement steel material.
    f_yk: MPA
        Characteristic yield strength of reinforcement [$MPa$].
    f_tk: MPA
        Characteristic tensile strength of reinforcement [$MPa$].
    eps_uk: PER_MILLE
        Characteristic strain of reinforcement at maximum load [$‰$].
    modulus_of_elasticity: MPA
        Young's modulus of the reinforcement steel [$MPa$] (default= 200000.0).
    density: KG_M3
        Unit mass of steel [$kg/m^3$] (default= 7850.0).
    poisson_ratio: RATIO
        Poisson's ratio in the elastic range [$-$] (default= 0.3).
    material_factor: DIMENSIONLESS
        Partial safety factor [$\gamma_s$] for reinforcement steel according to EN 1992-1-1 art.2.4.2.4 (default= 1.15).

    """

    name: str
    f_yk: MPA
    f_tk: MPA
    eps_uk: PER_MILLE
    modulus_of_elasticity: MPA = REBAR_STEEL_YOUNG_MODULUS
    density: KG_M3 = 7850.0
    poisson_ratio: RATIO = 0.3
    material_factor: DIMENSIONLESS = 1.15

    @property
    def f_yd(self) -> MPA:
        r"""[$f_{yd}$] Design yield strength of reinforcement (EN 1992-1-1:2004 art.3.2.7 (2)) [$MPa$].

        Returns
        -------
        MPA
            Example: 434.78 (for B500B)
        """
        return self.f_yk / self.material_factor

    @property
    def ductility_factor_k(self) -> DIMENSIONLESS:
        r"""Ductility factor k [$-$] -> ([$f_{tk}$] / [$f_{yk}$]) table C.1 Annex C from EN 1992-1-1:2004.

        Returns
        -------
        DIMENSIONLESS
            Example: 1.08 (for B500B)
        """
        return self.f_tk / self.f_yk

    @property
    def shear_modulus(self) -> MPA:
        r"""[$G$] Shear modulus of the reinforcement steel [$MPa$].

        Returns
        -------
        MPA
            Shear modulus of the material.
        """
        return self.modulus_of_elasticity / (2 * (1 + self.poisson_ratio))

    @classmethod
    def from_ec2(
        cls,
        steel_quality: ReinforcementSteelQuality = ReinforcementSteelQuality.B500B,
        *,
        name: str = "",
        modulus_of_elasticity: MPA = REBAR_STEEL_YOUNG_MODULUS,
        density: KG_M3 = 7850.0,
        poisson_ratio: RATIO = 0.3,
        material_factor: DIMENSIONLESS = 1.15,
    ) -> "ReinforcementSteel":
        r"""Build a reinforcement steel material from a steel quality according to Table C.1, Annex C of EN 1992-1-1:2004.

        All design-code logic lives in this factory; the resulting :class:`ReinforcementSteel` stores only data.

        Parameters
        ----------
        steel_quality: ReinforcementSteelQuality
            Enumeration of reinforcement steel qualities (default= B500B).
        name: str
            Name of the reinforcement steel material (default= steel quality name).
        modulus_of_elasticity: MPA
            Young's modulus of the reinforcement steel [$MPa$] (default= 200000.0).
        density: KG_M3
            Unit mass of steel [$kg/m^3$] (default= 7850.0).
        poisson_ratio: RATIO
            Poisson's ratio in the elastic range [$-$] (default= 0.3).
        material_factor: DIMENSIONLESS
            Partial safety factor [$\gamma_s$] for reinforcement steel (default= 1.15).

        Returns
        -------
        ReinforcementSteel
            Reinforcement steel material with the characteristics of the given quality.
        """
        value = steel_quality.value
        f_yk = float(value[1:-1])
        steel_class = value[-1].lower()
        ductility_factor_k = {"a": 1.05, "b": 1.08, "c": 1.15}[steel_class]
        eps_uk = {"a": 250.0, "b": 500.0, "c": 750.0}[steel_class]
        return cls(
            name=name if name else value,
            f_yk=f_yk,
            f_tk=f_yk * ductility_factor_k,
            eps_uk=eps_uk,
            modulus_of_elasticity=modulus_of_elasticity,
            density=density,
            poisson_ratio=poisson_ratio,
            material_factor=material_factor,
        )
