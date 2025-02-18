"""Module for concrete material properties."""

import math
import re
from dataclasses import dataclass, field
from enum import Enum

from blueprints.type_alias import DIMENSIONLESS, KG_M3, MM, MPA, PER_DEGREE, PER_MILLE, PERCENTAGE
from blueprints.unit_conversion import GPA_TO_MPA


class ConcreteAggregateType(Enum):
    """Enumeration of concrete aggregate types."""

    QUARTZITE = "Quartzite"
    LIMESTONE = "Limestone"
    SANDSTONE = "Sandstone"
    BASALT = "Basalt"


class CementClass(Enum):
    """Enumeration of cement class according to NEN-EN 1992-1-1 art.3.1.2 (6)."""

    S = "S"
    R = "R"
    N = "N"


class ConcreteStrengthClass(Enum):
    """Enumeration of concrete strength classes based on table 3.1 from NEN-EN 1992-1-1."""

    C12_15 = "C12/15"
    C16_20 = "C16/20"
    C20_25 = "C20/25"
    C25_30 = "C25/30"
    C30_37 = "C30/37"
    C35_45 = "C35/45"
    C40_50 = "C40/50"
    C45_55 = "C45/55"
    C50_60 = "C50/60"
    C55_67 = "C55/67"
    C60_75 = "C60/75"
    C70_85 = "C70/85"
    C80_95 = "C80/95"
    C90_105 = "C90/105"


class DiagramType(Enum):
    """Enumeration of diagram types of stress-strain relations."""

    BILINEAR = "Bi-Linear"
    PARABOLIC = "Parabolic"
    USER = "User defined"


class CementType(Enum):
    """Enumeration of CEM types."""

    CEM_I = "CEM I"
    CEM_II = "CEM II"
    CEM_III = "CEM III"
    CEM_III_A = "CEM IIIA"
    CEM_III_B = "CEM IIIB"
    CEM_III_C = "CEM IIIC"
    CEM_IV = "CEM IV"
    CEM_V = "CEM V"


@dataclass(frozen=True)
class ConcreteMaterial:
    r"""Representation of the strength and deformation characteristics for concrete material based on the analytical
    relation shown on table 3.1 from NEN-EN 1992-1-1.

    Parameters
    ----------
    concrete_class: ConcreteStrengthClass
        Enumeration of concrete strength classes (default: C30/37)
    cement_class: CementClass
        Cement class needed for calculation of Creep and shrinkage strain (Annex B from NEN-EN 1992-1-1). Classes are S, N and R. (default= N)
    density: KG_M3
        Unit mass of concrete [$kg/m^3$] (default= 2500.0 for regular reinforced concrete)
    diagram_type: DiagramType
        Type of stress-strain diagram (Figures 3.2, 3.3 and 3.4 from NEN-EN 1992-1-1) (default= Bi-Linear)
    aggregate_type: ConcreteAggregateType
        Type of aggregate in the concrete material (NEN-EN 1992-1-1) (default= Quartzite)
    aggregate_size: MM
        Largest nominal maximum aggregate size [$mm$] (NEN-EN 1992-1-1) (default= 16.0)
    use_plain_concrete_diagram: bool
        Use a Stress-strain diagram for plain or lightly reinforced concrete (NEN-EN 1992-1-1) (default= False)
    material_factor: DIMENSIONLESS
        Partial safety factor [$\gamma_c$] for concrete according to NEN-EN 1992-1-1 art.2.4.2.4 [$-$] (default= 1.5)
    thermal_coefficient: PER_DEGREE
        Thermal coefficient of the material [$1/°C$] (default= 1e-5)
    cement_type: CementType
        Type of cement in the concrete material (NEN-EN 1992-1-1) (default= CEM III)
    custom_name: str
        Use a custom name for the concrete material (default= concrete class name)
    custom_e_c: MPA
        Use a custom modulus of elasticity of concrete [$MPa$]
        If no custom value is given, the value [$E_{cm}$] from table 3.1 of NEN-EN 1992-1-1 is used.

    """

    concrete_class: ConcreteStrengthClass = field(default=ConcreteStrengthClass.C30_37)
    cement_class: CementClass = field(default=CementClass.N)
    density: KG_M3 = field(default=2500.0, metadata={"unit": "kg/m³"})
    diagram_type: DiagramType = field(default=DiagramType.BILINEAR)
    aggregate_type: ConcreteAggregateType = field(default=ConcreteAggregateType.QUARTZITE)
    aggregate_size: MM = field(default=16.0, metadata={"unit": "mm"})
    use_plain_concrete_diagram: bool = field(default=False)
    material_factor: DIMENSIONLESS = field(default=1.5)
    thermal_coefficient: PER_DEGREE = field(default=1e-5, metadata={"unit": "1/°C"})
    cement_type: CementType = field(default=CementType.CEM_III)
    custom_name: str | None = field(default=None, compare=False)
    custom_e_c: MPA | None = field(default=None, metadata={"unit": "MPa"})

    @property
    def name(self) -> str:
        """Name of the concrete material.

        Returns
        -------
        str
            Example: "C30/37"
        """
        if self.custom_name:
            return self.custom_name
        return self.concrete_class.value

    @property
    def e_c(self) -> MPA:
        r"""[$E_c$] Modulus of elasticity of concrete [$MPa$].

        If no custom value is given, the value [$E_{cm}$] from table 3.1 of NEN-EN 1992-1-1 is used.

        Returns
        -------
        MPA
            Example: 32836 (for C30/37)
        """
        if self.custom_e_c:
            return self.custom_e_c
        return self.e_cm

    @property
    def f_ck(self) -> MPA:
        r"""[$f_{ck}$] Characteristic compressive cylinder strength of concrete at 28 days [$MPa$].

        Returns
        -------
        MPA
            Example: 30 (for C30/37)
        """
        value = self.concrete_class.value
        if match := re.search(pattern=r"C(\d+)/", string=value):
            return int(match.group(1))
        raise ValueError("No match found for f_ck. Concrete class is invalid.")

    @property
    def f_ck_cube(self) -> MPA:
        r"""[$f_{ck,cube}$] Characteristic compressive cubic strength of concrete at 28 days [$MPa$].

        Returns
        -------
        MPA
            Example: 37 (for C30/37)
        """
        value = self.concrete_class.value
        if match := re.search(pattern=r"/(\d+)", string=value):
            return int(match.group(1))
        raise ValueError("No match found for f_ck_cube. Concrete class is invalid.")

    @property
    def f_cd(self) -> MPA:
        r"""[$f_{cd}$] Design value of concrete compressive strength (NEN-EN 1992-1-1 art.3.1.6 (1)) [$MPa$].

        Returns
        -------
        MPA
            Example: 20 (for C30/37)
        """
        return self.f_ck / self.material_factor

    @property
    def f_cm(self) -> MPA:
        r"""[$f_{cm}$] Mean value of concrete cylinder compressive strength [$MPa$].

        Returns
        -------
        MPA
            Example: 38 (for C30/37)
        """
        return self.f_ck + 8

    @property
    def f_cm_cube(self) -> MPA:
        r"""[$f_{cm,cube}$] Mean value of concrete cubic compressive strength [$MPa$].

        Returns
        -------
        MPA
            Example: 45 (for C30/37)
        """
        return self.f_ck_cube + 8

    @property
    def f_ctm(self) -> MPA:
        r"""[$f_{ctm}$] Mean value of axial tensile strength of concrete [$MPa$].

        Returns
        -------
        MPA
            Example: 2.896468153816889 (for C30/37)
        """
        if self.f_ck <= 50:
            return 0.30 * self.f_ck ** (2 / 3)
        return 2.12 * math.log(1 + (self.f_cm / 10))

    @property
    def sigma_cr(self) -> MPA:
        r"""[$\sigma_{cr}$] Crack tensile stress (long term) equal to [$0.6 \cdot f_{ctm}$] [$MPa$].

        Returns
        -------
        MPA
            Example: 1.7378808922901334 (for C30/37)
        """
        return self.f_ctm * 0.6

    @property
    def strain_cr(self) -> MPA:
        r"""[$\epsilon_{cr}$] Strain at crack tensile stress (long term) equal to [$\sigma_{cr} / E_{cm}$] [$MPa$].

        Returns
        -------
        MPA
            Example: 5.2926083941105295e-05 (for C30/37)
        """
        return self.sigma_cr / self.e_cm

    @property
    def f_ctk_0_05(self) -> MPA:
        r"""[$f_{ctk,0.05}$] Mean value of axial tensile strength of concrete, 5% fractile [$MPa$].

        Returns
        -------
        MPA
            Example: 2.027527707671822 (for C30/37)
        """
        return self.f_ctm * 0.7

    @property
    def f_ctd(self) -> MPA:
        r"""[$f_{ctd}$] Design value of tensile strength of concrete [$MPa$].

        Returns
        -------
        MPA
        Example: 1.3516851384478814 (for C30/37)
        """
        return self.f_ctk_0_05 / 1.5

    @property
    def f_ctk_0_95(self) -> MPA:
        r"""[$f_{ctk,0.95}$] Mean value of axial tensile strength of concrete, 95% fractile [$MPa$].

        Returns
        -------
        MPA
            Example: 3.765408599961956 (for C30/37)
        """
        return self.f_ctm * 1.3

    @property
    def e_cm(self) -> MPA:
        r"""[$E_{cm}$] Secant modulus of elasticity of concrete [$MPa$].

        Returns
        -------
        MPA
            Example: 32836 (for C30/37)
        """
        return int(22 * ((self.f_cm / 10) ** 0.3) * GPA_TO_MPA)

    @property
    def custom_e_c_present(self) -> bool:
        r"""Checks if the value of [$E_c$] equal is to the value of [$E_{cm}$] from table 3.1 of NEN-EN 1992-1-1.

        Returns
        -------
        bool
            Example: False if ConcreteMaterial.e_cm is equal to 32836 (for C30/37)
        """
        return self.e_c != self.e_cm

    @property
    def eps_c1(self) -> PER_MILLE:
        r"""[$\epsilon_{c1}$] Compressive strain in the concrete at the peak stress [$f_c$] [$‰$ (per mille)]. Value with a maximum of 2.8 ‰.
        Check Figure 3.2 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 2.1618768697354804 (for C30/37)
        """
        return min(0.7 * self.f_cm**0.31, 2.8)

    @property
    def eps_cu1(self) -> PER_MILLE:
        r"""[$\epsilon_{cu1}$] Nominal ultimate compressive strain in the concrete [$‰$ (per mille)]. Check Figure 3.2 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 3.5 (for C30/37)
        """
        if self.f_ck >= 50:
            return 2.8 + 27 * ((98 - self.f_cm) / 100) ** 4
        return 3.5

    @property
    def eps_c2(self) -> PER_MILLE:
        r"""[$\epsilon_{c2}$] Compressive strain at reaching the maximum strength according to Table 3.1 [$‰$ (per mille)].
        Check Figure 3.3 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 2.0 (for C30/37)
        """
        if self.f_ck >= 50:
            return 2.0 + 0.085 * (self.f_ck - 50) ** 0.53
        return 2.0

    @property
    def eps_cu2(self) -> PER_MILLE:
        r"""[$\epsilon_{cu2}$] Nominal ultimate compressive strain in the concrete according to Table 3.1 [$‰$ (per mille)].
        Check Figure 3.3 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 3.5 (for C30/37)
        """
        if self.f_ck >= 50:
            return 2.6 + 35 * ((90 - self.f_ck) / 100) ** 4
        return 3.5

    @property
    def n_factor(self) -> DIMENSIONLESS:
        r"""[$n$] factor from table 3.1 of NEN-EN 1992-1-1 [$-$].

        Returns
        -------
        DIMENSIONLESS
            Example: 2.0 (for C30/37)
        """
        if self.f_ck >= 50:
            return 1.4 + 23.4 * ((90 - self.f_ck) / 100) ** 4
        return 2.0

    @property
    def eps_c3(self) -> PER_MILLE:
        r"""[$\epsilon_{c3}$] Compressive strain at reaching the maximum strength according to Bi-linear stress-strain relation [$‰$ (per mille)].

        Check Figure 3.4 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 1.75 (for C30/37)
        """
        if self.f_ck >= 50:
            return 1.75 + 0.55 * ((self.f_ck - 50) / 40)
        return 1.75

    @property
    def eps_cu3(self) -> PER_MILLE:
        r"""[$\epsilon_{cu3}$] Nominal ultimate compressive strain in concrete according to Bi-linear stress-strain relation [$‰$ (per mille)].

        Check Figure 3.4 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 3.5 (for C30/37)
        """
        if self.f_ck >= 50:
            return 2.6 + 35 * ((90 - self.f_ck) / 100) ** 4
        return 3.5

    def rho_min(self, f_yd: MPA) -> PERCENTAGE:
        r"""[$\rho_{min}$] Minimum reinforcement ratio (CB2, 7de druk 2011, pag.55) [$%$].

        Parameters
        ----------
        f_yd: MPA
            Design yield strength of reinforcement [$MPa$]

        Returns
        -------
        PERCENTAGE
        """
        return (0.223 * (self.f_ctm / f_yd)) * 100
