"""Module for concrete material properties."""

from dataclasses import dataclass, field
from enum import Enum

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import (
    SteelStrengthClass,
    Table3Dot1NominalValuesHotRolledStructuralSteel,
)
from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MPA, PER_DEGREE

# default data from NEN-EN 1992-1-1 3.1.1(1)
STEEL_YOUNG_MODULUS = 210_000.0  # [MPa]
STEEL_POISSON_RATIO = 0.3  # [-]
STEEL_THERMAL_COEFFICIENT = 1.2e-5  # [1/°C]


class DiagramType(Enum):
    """Enumeration of diagram types of stress-strain relations."""

    BI_LINEAR = "Bi-Linear"
    PARABOLIC = "Parabolic"


@dataclass(frozen=True)
class SteelMaterial:
    r"""Representation of the strength and deformation characteristics for steel material.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    density: KG_M3
        Unit mass of steel [$kg/m^3$] (default= 7850.0)
    diagram_type: DiagramType
        Type of stress-strain diagram (default= Bi-Linear)
    quality_class: str
        Quality class of the steel material (default= None)
    custom_name: str
        Use a custom name for the steel material (default= steel class name)
    custom_e_modulus: MPA
        Use a custom modulus of elasticity of steel [$MPa$]
        If no custom value is given, the value [$E$] from standard tables is used.
    custom_poisson_ratio: DIMENSIONLESS
        Use a custom Poisson's ratio for the steel material (default= 0.3)
    custom_thermal_coefficient: PER_DEGREE
        Use a custom thermal coefficient for the steel material (default= 1.2e-5)
    custom_yield_strength: MPA
        Use a custom yield strength for the steel material (default= None)
    custom_ultimate_strength: MPA
        Use a custom ultimate strength for the steel material (default= None)

    """

    steel_class: SteelStrengthClass = field(default=SteelStrengthClass.S355)
    density: KG_M3 = field(default=7850.0, metadata={"unit": "kg/m³"})
    diagram_type: DiagramType = field(default=DiagramType.BI_LINEAR)
    quality_class: str | None = field(default=None)
    custom_name: str | None = field(default=None, compare=False)
    custom_e_modulus: MPA | None = field(default=None, metadata={"unit": "MPa"})
    custom_poisson_ratio: DIMENSIONLESS | None = field(default=None)
    custom_thermal_coefficient: PER_DEGREE | None = field(default=None)
    custom_yield_strength: MPA | None = field(default=None)
    custom_ultimate_strength: MPA | None = field(default=None)

    @property
    def name(self) -> str:
        """Name of the steel material.

        Returns
        -------
        str
            Example: "S355"
        """
        if self.custom_name:
            return self.custom_name
        standard_group = self.steel_class.value[0].value
        steel_class = self.steel_class.value[1]
        return f"{steel_class} ({standard_group})"

    @property
    def e_modulus(self) -> MPA:
        """Modulus of elasticity of the steel material.

        Returns
        -------
        MPA
            Modulus of elasticity of steel [$MPa$]
        """
        if self.custom_e_modulus:
            return self.custom_e_modulus
        return STEEL_YOUNG_MODULUS

    @property
    def poisson_ratio(self) -> DIMENSIONLESS:
        """Poisson's ratio of the steel material.

        Returns
        -------
        DIMENSIONLESS
            Poisson's ratio of the material
        """
        if self.custom_poisson_ratio:
            return self.custom_poisson_ratio
        return STEEL_POISSON_RATIO

    @property
    def thermal_coefficient(self) -> PER_DEGREE:
        """Thermal coefficient of the steel material [1/°C].

        Returns
        -------
        PER_DEGREE
            Thermal coefficient of the material
        """
        if self.custom_thermal_coefficient:
            return self.custom_thermal_coefficient
        return STEEL_THERMAL_COEFFICIENT

    @property
    def shear_modulus(self) -> MPA:
        """Shear modulus of the steel material.

        Returns
        -------
        MPA
            Shear modulus of the material
        """
        return self.e_modulus / (2 * (1 + self.poisson_ratio))

    def yield_strength(self, thickness: MM) -> MPA | None:
        """Yield strength of the steel material for steel [$f_y$].

        Parameters
        ----------
        thickness: MM
            Nominal thickness of the steel element [$mm$]

        Returns
        -------
        MPA | None
            Yield strength of the material at the given temperature
        """
        if self.custom_yield_strength:
            return self.custom_yield_strength
        return Table3Dot1NominalValuesHotRolledStructuralSteel(steel_class=self.steel_class, thickness=thickness).fy

    def ultimate_strength(self, thickness: MM) -> MPA | None:
        """Ultimate strength of the steel material for steel [$f_u$].

        Parameters
        ----------
        thickness: MM
            Nominal thickness of the steel element [$mm$]

        Returns
        -------
        MPA | None
            Ultimate strength of the material at the given temperature
        """
        if self.custom_ultimate_strength:
            return self.custom_ultimate_strength
        return Table3Dot1NominalValuesHotRolledStructuralSteel(steel_class=self.steel_class, thickness=thickness).fu
