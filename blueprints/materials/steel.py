"""Module for steel material properties."""

import contextlib
from dataclasses import dataclass, field
from enum import Enum

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import (
    SteelStrengthClass,
    Table3Dot1NominalValuesHotRolledStructuralSteel,
)
from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MPA, PER_DEGREE, RATIO

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


@dataclass(frozen=True)
class StrengthRow:
    r"""One row of a thickness-dependent strength table of a steel material.

    Parameters
    ----------
    max_thickness: MM
        Inclusive upper bound of the nominal thickness for which this row applies [$mm$].
    strength: MPA
        Characteristic strength for this thickness range [$MPa$].

    """

    max_thickness: MM
    strength: MPA


@dataclass(frozen=True)
class Steel:
    r"""Code-agnostic data container for the strength and deformation characteristics of steel.

    The container is independent of any design code: the thickness-dependent strengths are stored
    as two tables of :class:`StrengthRow` entries (one for the yield strength and one for the
    ultimate tensile strength), so international alloys can be created directly through the
    constructor. The thickness is unknown when the material is defined; the corresponding strengths
    are looked up afterwards with :meth:`f_yk` and :meth:`f_uk`. Use :meth:`from_en10025` to build
    an instance from a NEN-EN 1993-1-1 Table 3.1 grade.

    Parameters
    ----------
    name: str
        Name of the steel material.
    f_y_table: tuple[StrengthRow, ...]
        Thickness-dependent table of characteristic yield strengths, ordered by ascending maximum thickness.
    f_u_table: tuple[StrengthRow, ...]
        Thickness-dependent table of characteristic ultimate tensile strengths, ordered by ascending maximum thickness.
    density: KG_M3
        Unit mass of steel [$kg/m^3$] (default= 7850.0).
    e_modulus: MPA
        Young's modulus of steel [$MPa$] (default= 210000.0).
    poisson_ratio: RATIO
        Poisson's ratio in the elastic range [$-$] (default= 0.3).
    thermal_coefficient: PER_DEGREE
        Thermal coefficient of the material [$1/°C$] (default= 1.2e-5).
    material_factor: DIMENSIONLESS
        Partial factor [$\gamma_{m0}$] for resistance of cross-sections according to NEN-EN 1993-1-1 art.6.1 (default= 1.0).

    """

    name: str
    f_y_table: tuple[StrengthRow, ...]
    f_u_table: tuple[StrengthRow, ...]
    density: KG_M3 = 7850.0
    e_modulus: MPA = STEEL_YOUNG_MODULUS
    poisson_ratio: RATIO = STEEL_POISSON_RATIO
    thermal_coefficient: PER_DEGREE = STEEL_THERMAL_COEFFICIENT
    material_factor: DIMENSIONLESS = 1.0

    @property
    def modulus_of_elasticity(self) -> MPA:
        """Young's modulus of steel [$MPa$].

        Returns
        -------
        MPA
            Modulus of elasticity of the material.
        """
        return self.e_modulus

    @property
    def shear_modulus(self) -> MPA:
        """Shear modulus of steel [$MPa$].

        Returns
        -------
        MPA
            Shear modulus of the material.
        """
        return self.e_modulus / (2 * (1 + self.poisson_ratio))

    def f_yk(self, thickness: MM) -> MPA:
        r"""[$f_{yk}$] Characteristic yield strength of the steel material for the given nominal thickness [$MPa$].

        Parameters
        ----------
        thickness: MM
            Nominal thickness of the element [$mm$].

        Returns
        -------
        MPA
            Characteristic yield strength.
        """
        return self._lookup(self.f_y_table, thickness).strength

    def f_uk(self, thickness: MM) -> MPA:
        r"""[$f_{uk}$] Characteristic ultimate tensile strength of the steel material for the given nominal thickness [$MPa$].

        Parameters
        ----------
        thickness: MM
            Nominal thickness of the element [$mm$].

        Returns
        -------
        MPA
            Characteristic ultimate tensile strength.
        """
        return self._lookup(self.f_u_table, thickness).strength

    def f_yd(self, thickness: MM) -> MPA:
        r"""[$f_{yd}$] Design yield strength of the steel material for the given nominal thickness [$MPa$].

        Parameters
        ----------
        thickness: MM
            Nominal thickness of the element [$mm$].

        Returns
        -------
        MPA
            Design yield strength, i.e. the characteristic yield strength divided by the stored partial factor.
        """
        return self.f_yk(thickness) / self.material_factor

    def _lookup(self, table: tuple[StrengthRow, ...], thickness: MM) -> StrengthRow:
        """Find the row of the given strength table that applies to the given nominal thickness.

        Parameters
        ----------
        table: tuple[StrengthRow, ...]
            Strength table to search.
        thickness: MM
            Nominal thickness of the element [$mm$].

        Returns
        -------
        StrengthRow
            The applicable strength row.
        """
        if thickness <= 0:
            raise ValueError(f"Thickness must be positive, got {thickness} mm")
        for row in sorted(table, key=lambda candidate: candidate.max_thickness):
            if thickness <= row.max_thickness:
                return row
        raise ValueError(f"{self.name} is only available for thicknesses up to {max(row.max_thickness for row in table)} mm")

    @classmethod
    def from_en10025(
        cls,
        grade: SteelStrengthClass = SteelStrengthClass.S355,
        *,
        name: str = "",
        density: KG_M3 = 7850.0,
        e_modulus: MPA = STEEL_YOUNG_MODULUS,
        poisson_ratio: RATIO = STEEL_POISSON_RATIO,
        thermal_coefficient: PER_DEGREE = STEEL_THERMAL_COEFFICIENT,
        material_factor: DIMENSIONLESS = 1.0,
    ) -> "Steel":
        r"""Build a steel material from a grade according to Table 3.1 of NEN-EN 1993-1-1.

        The thickness-dependent strengths are read from :class:`Table3Dot1NominalValuesHotRolledStructuralSteel`
        for the [$\leq 40\ mm$] band and, when specified for the grade, the [$> 40\ mm$] (up to 80 mm) band.

        Parameters
        ----------
        grade: SteelStrengthClass
            Enumeration of steel strength classes (default= S355).
        name: str
            Name of the steel material (default= grade display name and standard group).
        density: KG_M3
            Unit mass of steel [$kg/m^3$] (default= 7850.0).
        e_modulus: MPA
            Young's modulus of steel [$MPa$] (default= 210000.0).
        poisson_ratio: RATIO
            Poisson's ratio in the elastic range [$-$] (default= 0.3).
        thermal_coefficient: PER_DEGREE
            Thermal coefficient of the material [$1/°C$] (default= 1.2e-5).
        material_factor: DIMENSIONLESS
            Partial factor [$\gamma_{m0}$] for resistance of cross-sections (default= 1.0).

        Returns
        -------
        Steel
            Steel material with the characteristics of the given grade.
        """
        thin = Table3Dot1NominalValuesHotRolledStructuralSteel(steel_class=grade, thickness=40)
        f_y_rows = [StrengthRow(max_thickness=40.0, strength=thin.fy)]
        f_u_rows = [StrengthRow(max_thickness=40.0, strength=thin.fu)]
        # The >40 mm (up to 80 mm) band is not specified for every grade (e.g. NEN-EN 10219-1);
        # accessing fy/fu then raises a ValueError and the band is simply omitted.
        with contextlib.suppress(ValueError):
            thick = Table3Dot1NominalValuesHotRolledStructuralSteel(steel_class=grade, thickness=80)
            f_y_rows.append(StrengthRow(max_thickness=80.0, strength=thick.fy))
            f_u_rows.append(StrengthRow(max_thickness=80.0, strength=thick.fu))
        standard_group = grade.value[0].value
        return cls(
            name=name if name else f"{grade.value[1]} ({standard_group})",
            f_y_table=tuple(f_y_rows),
            f_u_table=tuple(f_u_rows),
            density=density,
            e_modulus=e_modulus,
            poisson_ratio=poisson_ratio,
            thermal_coefficient=thermal_coefficient,
            material_factor=material_factor,
        )
