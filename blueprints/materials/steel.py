"""Module for concrete material properties."""

from dataclasses import dataclass, field
from enum import Enum

from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MPA, PER_DEGREE

# default data from NEN-EN 1992-1-1 3.1.1(1)
STEEL_YOUNG_MODULUS = 210_000.0  # [MPa]
STEEL_POISSON_RATIO = 0.3  # [-]
STEEL_THERMAL_COEFFICIENT = 1.2e-5  # [1/°C]

# define error messages for yield strength and ultimate strength
ERROR40 = ValueError("Yield strength not defined for thickness > 40 mm")
ERROR80 = ValueError("Yield strength not defined for thickness > 80 mm")


class SteelStrengthClass(Enum):
    """Enumeration of steel strength classes based on standard tables, based on Table 3.1 from NEN-EN 1993-1-1."""

    # data from NEN-EN 10025-2
    EN_10025_2_S235 = "NEN-EN 10025-2 S 235"
    EN_10025_2_S275 = "NEN-EN 10025-2 S 275"
    EN_10025_2_S355 = "NEN-EN 10025-2 S 355"
    EN_10025_2_S450 = "NEN-EN 10025-2 S 450"

    # data from NEN-EN 10025-3
    EN_10025_3_S275_N_NL = "NEN-EN 10025-3 S 275 N/NL"
    EN_10025_3_S355_N_NL = "NEN-EN 10025-3 S 355 N/NL"
    EN_10025_3_S420_N_NL = "NEN-EN 10025-3 S 420 N/NL"
    EN_10025_3_S460_N_NL = "NEN-EN 10025-3 S 460 N/NL"

    # data from NEN-EN 10025-4
    EN_10025_4_S275_M_ML = "NEN-EN 10025-4 S 275 M/ML"
    EN_10025_4_S355_M_ML = "NEN-EN 10025-4 S 355 M/ML"
    EN_10025_4_S420_M_ML = "NEN-EN 10025-4 S 420 M/ML"
    EN_10025_4_S460_M_ML = "NEN-EN 10025-4 S 460 M/ML"

    # data from NEN-EN 10025-5
    EN_10025_5_S235_W = "NEN-EN 10025-5 S 235 W"
    EN_10025_5_S355_W = "NEN-EN 10025-5 S 355 W"

    # data from NEN-EN 10025-6
    EN_10025_6_S460_Q_QL_QL1 = "NEN-EN 10025-6 S 460 Q/QL/QL1"

    # data from EN 10210-1
    EN_10210_1_S235_H = "EN 10210-1 S 235 H"
    EN_10210_1_S275_H = "EN 10210-1 S 275 H"
    EN_10210_1_S355_H = "EN 10210-1 S 355 H"
    EN_10210_1_S275_NH_NLH = "EN 10210-1 S 275 NH/NLH"
    EN_10210_1_S355_NH_NLH = "EN 10210-1 S 355 NH/NLH"
    EN_10210_1_S420_NH_NHL = "EN 10210-1 S 420 NH/NHL"
    EN_10210_1_S460_NH_NLH = "EN 10210-1 S 460 NH/NLH"

    # data from EN 10219-1
    EN_10219_1_S235_H = "EN 10219-1 S 235 H"
    EN_10219_1_S275_H = "EN 10219-1 S 275 H"
    EN_10219_1_S355_H = "EN 10219-1 S 355 H"
    EN_10219_1_S275_NH_NLH = "EN 10219-1 S 275 NH/NLH"
    EN_10219_1_S355_NH_NLH = "EN 10219-1 S 355 NH/NLH"
    EN_10219_1_S460_NH_NLH = "EN 10219-1 S 460 NH/NLH"
    EN_10219_1_S275_MH_MLH = "EN 10219-1 S 275 MH/MLH"
    EN_10219_1_S355_MH_MLH = "EN 10219-1 S 355 MH/MLH"
    EN_10219_1_S420_MH_MLH = "EN 10219-1 S 420 MH/MLH"
    EN_10219_1_S460_MH_MLH = "EN 10219-1 S 460 MH/MLH"


class DiagramType(Enum):
    """Enumeration of diagram types of stress-strain relations."""

    BILINEAR = "Bi-Linear"
    PARABOLIC = "Parabolic"
    USER = "User defined"


@dataclass(frozen=True)
class SteelMaterial:
    r"""Representation of the strength and deformation characteristics for steel material.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    thickness:
        Nominal thickness of the steel element [$mm$] (default: 10.0)
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

    steel_class: SteelStrengthClass = field(default=SteelStrengthClass.EN_10025_2_S355)
    thickness: MM = field(default=10.0, metadata={"unit": "mm"})
    density: KG_M3 = field(default=7850.0, metadata={"unit": "kg/m³"})
    diagram_type: DiagramType = field(default=DiagramType.BILINEAR)
    quality_class: str | None = field(default=None)
    custom_name: str | None = field(default=None, compare=False)
    custom_e_modulus: MPA | None = field(default=None, metadata={"unit": "GPa"})
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
        return self.steel_class.value

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
        """Thermal coefficient of the steel material.

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

    def yield_strength(self) -> MPA:  # noqa: C901, PLR0911, PLR0912, PLR0915
        """Yield strength of the steel material for steel.

        Returns
        -------
        MPA
            Yield strength of the material at the given temperature
        """
        if self.custom_yield_strength:
            return float(self.custom_yield_strength)

        match self.steel_class:
            case SteelStrengthClass.EN_10025_2_S235:
                if self.thickness > 80:
                    raise ERROR80
                return 235.0 if self.thickness <= 40 else 215.0
            case SteelStrengthClass.EN_10025_2_S275:
                if self.thickness > 80:
                    raise ERROR80
                return 275.0 if self.thickness <= 40 else 255.0
            case SteelStrengthClass.EN_10025_2_S355:
                if self.thickness > 80:
                    raise ERROR80
                return 355.0 if self.thickness <= 40 else 335.0
            case SteelStrengthClass.EN_10025_2_S450:
                if self.thickness > 80:
                    raise ERROR80
                return 440.0 if self.thickness <= 40 else 410.0
            case SteelStrengthClass.EN_10025_3_S275_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 275.0 if self.thickness <= 40 else 255.0
            case SteelStrengthClass.EN_10025_3_S355_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 355.0 if self.thickness <= 40 else 335.0
            case SteelStrengthClass.EN_10025_3_S420_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 420.0 if self.thickness <= 40 else 390.0
            case SteelStrengthClass.EN_10025_3_S460_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 460.0 if self.thickness <= 40 else 430.0
            case SteelStrengthClass.EN_10025_4_S275_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 275.0 if self.thickness <= 40 else 255.0
            case SteelStrengthClass.EN_10025_4_S355_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 355.0 if self.thickness <= 40 else 335.0
            case SteelStrengthClass.EN_10025_4_S420_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 420.0 if self.thickness <= 40 else 390.0
            case SteelStrengthClass.EN_10025_4_S460_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 460.0 if self.thickness <= 40 else 430.0
            case SteelStrengthClass.EN_10025_5_S235_W:
                if self.thickness > 80:
                    raise ERROR80
                return 235.0 if self.thickness <= 40 else 215.0
            case SteelStrengthClass.EN_10025_5_S355_W:
                if self.thickness > 80:
                    raise ERROR80
                return 355.0 if self.thickness <= 40 else 335.0
            case SteelStrengthClass.EN_10025_6_S460_Q_QL_QL1:
                if self.thickness > 80:
                    raise ERROR80
                return 460.0 if self.thickness <= 40 else 440.0
            case SteelStrengthClass.EN_10210_1_S235_H:
                if self.thickness > 80:
                    raise ERROR80
                return 235.0 if self.thickness <= 40 else 215.0
            case SteelStrengthClass.EN_10210_1_S275_H:
                if self.thickness > 80:
                    raise ERROR80
                return 275.0 if self.thickness <= 40 else 255.0
            case SteelStrengthClass.EN_10210_1_S355_H:
                if self.thickness > 80:
                    raise ERROR80
                return 355.0 if self.thickness <= 40 else 335.0
            case SteelStrengthClass.EN_10210_1_S275_NH_NLH:
                if self.thickness > 80:
                    raise ERROR80
                return 275.0 if self.thickness <= 40 else 255.0
            case SteelStrengthClass.EN_10210_1_S355_NH_NLH:
                if self.thickness > 80:
                    raise ERROR80
                return 355.0 if self.thickness <= 40 else 335.0
            case SteelStrengthClass.EN_10210_1_S420_NH_NHL:
                if self.thickness > 80:
                    raise ERROR80
                return 420.0 if self.thickness <= 40 else 390.0
            case SteelStrengthClass.EN_10210_1_S460_NH_NLH:
                if self.thickness > 80:
                    raise ERROR80
                return 460.0 if self.thickness <= 40 else 430.0
            case SteelStrengthClass.EN_10219_1_S235_H:
                if self.thickness > 40:
                    raise ERROR40
                return 235.0
            case SteelStrengthClass.EN_10219_1_S275_H:
                if self.thickness > 40:
                    raise ERROR40
                return 275.0
            case SteelStrengthClass.EN_10219_1_S355_H:
                if self.thickness > 40:
                    raise ERROR40
                return 355.0
            case SteelStrengthClass.EN_10219_1_S275_NH_NLH:
                if self.thickness > 40:
                    raise ERROR40
                return 275.0
            case SteelStrengthClass.EN_10219_1_S355_NH_NLH:
                if self.thickness > 40:
                    raise ERROR40
                return 355.0
            case SteelStrengthClass.EN_10219_1_S460_NH_NLH:
                if self.thickness > 40:
                    raise ERROR40
                return 460.0
            case SteelStrengthClass.EN_10219_1_S275_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 275.0
            case SteelStrengthClass.EN_10219_1_S355_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 355.0
            case SteelStrengthClass.EN_10219_1_S420_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 420.0
            case SteelStrengthClass.EN_10219_1_S460_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 460.0
            case _:
                raise ValueError("Unknown steel strength class")

    def ultimate_strength(self) -> MPA:  # noqa: C901, PLR0911, PLR0912, PLR0915
        """Ultimate strength of the steel material for steel.

        Returns
        -------
        MPA
            Ultimate strength of the material at the given temperature
        """
        if self.custom_ultimate_strength:
            return float(self.custom_ultimate_strength)

        match self.steel_class:
            case SteelStrengthClass.EN_10025_2_S235:
                if self.thickness > 80:
                    raise ERROR80
                return 360.0 if self.thickness <= 40 else 360.0  # noqa: RUF034
            case SteelStrengthClass.EN_10025_2_S275:
                if self.thickness > 80:
                    raise ERROR80
                return 430.0 if self.thickness <= 40 else 410.0
            case SteelStrengthClass.EN_10025_2_S355:
                if self.thickness > 80:
                    raise ERROR80
                return 510.0 if self.thickness <= 40 else 470.0
            case SteelStrengthClass.EN_10025_2_S450:
                if self.thickness > 80:
                    raise ERROR80
                return 550.0 if self.thickness <= 40 else 550.0  # noqa: RUF034
            case SteelStrengthClass.EN_10025_3_S275_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 390.0 if self.thickness <= 40 else 370.0
            case SteelStrengthClass.EN_10025_3_S355_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 490.0 if self.thickness <= 40 else 470.0
            case SteelStrengthClass.EN_10025_3_S420_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 520.0 if self.thickness <= 40 else 520.0  # noqa: RUF034
            case SteelStrengthClass.EN_10025_3_S460_N_NL:
                if self.thickness > 80:
                    raise ERROR80
                return 540.0 if self.thickness <= 40 else 540.0  # noqa: RUF034
            case SteelStrengthClass.EN_10025_4_S275_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 370.0 if self.thickness <= 40 else 360.0
            case SteelStrengthClass.EN_10025_4_S355_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 470.0 if self.thickness <= 40 else 450.0
            case SteelStrengthClass.EN_10025_4_S420_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 520.0 if self.thickness <= 40 else 500.0
            case SteelStrengthClass.EN_10025_4_S460_M_ML:
                if self.thickness > 80:
                    raise ERROR80
                return 540.0 if self.thickness <= 40 else 530.0
            case SteelStrengthClass.EN_10025_5_S235_W:
                if self.thickness > 80:
                    raise ERROR80
                return 360.0 if self.thickness <= 40 else 340.0
            case SteelStrengthClass.EN_10025_5_S355_W:
                if self.thickness > 80:
                    raise ERROR80
                return 510.0 if self.thickness <= 40 else 490.0
            case SteelStrengthClass.EN_10025_6_S460_Q_QL_QL1:
                if self.thickness > 80:
                    raise ERROR80
                return 570.0 if self.thickness <= 40 else 550.0
            case SteelStrengthClass.EN_10210_1_S235_H:
                if self.thickness > 80:
                    raise ERROR80
                return 360.0 if self.thickness <= 40 else 340.0
            case SteelStrengthClass.EN_10210_1_S275_H:
                if self.thickness > 80:
                    raise ERROR80
                return 430.0 if self.thickness <= 40 else 410.0
            case SteelStrengthClass.EN_10210_1_S355_H:
                if self.thickness > 80:
                    raise ERROR80
                return 510.0 if self.thickness <= 40 else 490.0
            case SteelStrengthClass.EN_10210_1_S275_NH_NLH:
                if self.thickness > 80:
                    raise ERROR80
                return 390.0 if self.thickness <= 40 else 370.0
            case SteelStrengthClass.EN_10210_1_S355_NH_NLH:
                if self.thickness > 80:
                    raise ERROR80
                return 490.0 if self.thickness <= 40 else 470.0
            case SteelStrengthClass.EN_10210_1_S420_NH_NHL:
                if self.thickness > 80:
                    raise ERROR80
                return 540.0 if self.thickness <= 40 else 520.0
            case SteelStrengthClass.EN_10210_1_S460_NH_NLH:
                if self.thickness > 80:
                    raise ERROR80
                return 560.0 if self.thickness <= 40 else 550.0
            case SteelStrengthClass.EN_10219_1_S235_H:
                if self.thickness > 40:
                    raise ERROR40
                return 360.0
            case SteelStrengthClass.EN_10219_1_S275_H:
                if self.thickness > 40:
                    raise ERROR40
                return 430.0
            case SteelStrengthClass.EN_10219_1_S355_H:
                if self.thickness > 40:
                    raise ERROR40
                return 510.0
            case SteelStrengthClass.EN_10219_1_S275_NH_NLH:
                if self.thickness > 40:
                    raise ERROR40
                return 370.0
            case SteelStrengthClass.EN_10219_1_S355_NH_NLH:
                if self.thickness > 40:
                    raise ERROR40
                return 470.0
            case SteelStrengthClass.EN_10219_1_S460_NH_NLH:
                if self.thickness > 40:
                    raise ERROR40
                return 550.0
            case SteelStrengthClass.EN_10219_1_S275_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 360.0
            case SteelStrengthClass.EN_10219_1_S355_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 470.0
            case SteelStrengthClass.EN_10219_1_S420_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 500.0
            case SteelStrengthClass.EN_10219_1_S460_MH_MLH:
                if self.thickness > 40:
                    raise ERROR40
                return 530.0
            case _:
                raise ValueError("Unknown steel strength class")
