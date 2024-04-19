"""Module for concrete material properties."""

import math
import re
from dataclasses import dataclass
from enum import Enum

from blueprints.type_alias import DIMENSIONLESS, KG, MM, MPA, PER_MILLE, PERCENTAGE
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
    """Enumeration of concrete strength classes based on tabel 3.1 from NEN-EN 1992-1-1."""

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


@dataclass
class ConcreteMaterial:
    """Representation of the strength and deformation characteristics for concrete material based on the analytical
    relation shown on tabel 3.1 from NEN-EN 1992-1-1.
    """

    def __init__(  # noqa: PLR0913
        self,
        concrete_class: ConcreteStrengthClass = ConcreteStrengthClass.C30_37,
        name: str = "",
        e_c: MPA | None = None,
        cement_class: CementClass = CementClass.N,
        density: KG_M3 = 2500.0,
        diagram_type: DiagramType = DiagramType.BILINEAR,
        aggregate_type: ConcreteAggregateType = ConcreteAggregateType.QUARTZITE,
        aggregate_size: MM = 16.0,
        plain_concrete_diagram: bool = False,
        material_factor: DIMENSIONLESS = 1.5,
        thermal_coefficient: DIMENSIONLESS = 1e-5,
        cement_type: CementType = CementType.CEM_III,
    ) -> None:
        """Initializes a ConcreteMaterial object.

        Parameters
        ----------
        concrete_class: ConcreteStrengthClass
            Enumeration of concrete strength classes (default: C30/37)
        name: str
            Name of the concrete material (default= concrete class name)
        e_c: MPA
            Use a custom modulus of elasticity of concrete [MPa]
            If none is given the value from table 3.1 (Ecm) of NEN-EN 1992-1-1 is used.
        cement_class: CementClass
            Enumeration of cement class (default= N)
        density: KG_M3
            Density in [kg/m³] (default= 2500.0)
        diagram_type: DiagramType
            Enumeration of diagram types of stress-strain relations (default= Bi-Linear)
        aggregate_type: ConcreteAggregateType
            Enumeration of concrete aggregate types (default= Quartzite)
        aggregate_size: MM
            Largest nominal maximum aggregate size [mm] (NEN-EN 1992-1-1) (default= 16.0)
        plain_concrete_diagram: bool
            Use a Stress-strain diagram for plain or lightly reinforced concrete (NEN-EN 1992-1-1) (default= False)
        material_factor: DIMENSIONLESS
            Partial safety factor (yc) for concrete according to NEN-EN 1992-1-1 art.2.4.2.4 (default= 1.5)
        thermal_coefficient: DIMENSIONLESS
            Thermal coefficient of the material [-] (default= 1e-5)
        cement_type: CementType
            Cement types (default= CEM I)

        """
        self._e_c = e_c
        self._cement_class: CementClass = cement_class
        self._concrete_class: ConcreteStrengthClass = concrete_class
        self._name: str = name
        self._density: float = density
        self._diagram_type: DiagramType = diagram_type
        self._aggregate_type: ConcreteAggregateType = aggregate_type
        self._aggregate_size: float = aggregate_size
        self._plain_concrete_diagram: bool = plain_concrete_diagram
        self._material_factor: float = material_factor
        self._thermal_coefficient = thermal_coefficient
        self._cement_type: CementType = cement_type

    @property
    def name(self) -> str:
        """Name of the concrete material.

        Returns
        -------
        str
            Example: "C30/37"
        """
        if self._name:
            return self._name
        return self._concrete_class.value

    @property
    def e_c(self) -> MPA:
        """Modulus of elasticity of concrete [MPa].

        If no custom value is given, the value from table 3.1 of NEN-EN 1992-1-1 is used.

        Returns
        -------
        MPA
            Example: 32836 (for C30/37)
        """
        if self._e_c:
            return self._e_c
        return self.e_cm

    @property
    def concrete_class(self) -> ConcreteStrengthClass:
        """Concrete class of the ConcreteMaterial object.

        Returns
        -------
        ConcreteStrengthClass
            Example: "ConcreteStrengthClass.C30_37"
        """
        return self._concrete_class

    @property
    def material_factor(self) -> DIMENSIONLESS:
        """Partial safety factor (yc) for concrete according to NEN-EN 1992-1-1 art.2.4.2.4[-].

        Returns
        -------
        DIMENSIONLESS
            Example: 1.5
        """
        return self._material_factor

    @property
    def thermal_coefficient(self) -> DIMENSIONLESS:
        """Thermal coefficient of the material [-].

        Returns
        -------
        DIMENSIONLESS
            Example: 1e-5
        """
        return self._thermal_coefficient

    @property
    def f_ck(self) -> MPA:
        """Characteristic compressive cylinder strength of concrete at 28 days [MPa].

        Returns
        -------
        MPA
            Example: 30 (for C30/37)
        """
        value = self._concrete_class.value
        match = re.search(pattern=r"C(\d+)/", string=value)
        assert match
        return int(match.group(1))

    @property
    def f_ck_cube(self) -> MPA:
        """Characteristic compressive cubic strength of concrete_checks at 28 days [MPa].

        Returns
        -------
        MPA
            Example: 37 (for C30/37)
        """
        value = self._concrete_class.value
        match = re.search(pattern=r"/(\d+)", string=value)
        assert match
        return int(match.group(1))

    @property
    def f_cd(self) -> MPA:
        """Design compressive cylinder strength of concrete_checks at 28 days (NEN-EN 1992-1-1 art.3.1.6 (1)) [MPa].

        Returns
        -------
        MPA
            Example: 20 (for C30/37)
        """
        return self.f_ck / self.material_factor

    @property
    def f_cm(self) -> MPA:
        """Mean value of concrete cylinder compressive strength [MPa].

        Returns
        -------
        MPA
            Example: 38 (for C30/37)
        """
        return self.f_ck + 8

    @property
    def f_cm_cube(self) -> MPA:
        """Mean value of concrete_checks cubic compressive strength [MPa].

        Returns
        -------
        MPA
            Example: 45 (for C30/37)
        """
        return self.f_ck_cube + 8

    @property
    def f_ctm(self) -> MPA:
        """Mean value of axial tensile strength of concrete [MPa].

        Returns
        -------
        MPA
            Example: 2,9 (for C30/37)
        """
        if self.f_ck <= 50:
            return 0.30 * self.f_ck ** (2 / 3)
        return 2.12 * math.log(1 + (self.f_cm / 10))

    @property
    def sigma_cr(self) -> MPA:
        """Crack tensile stress (long term) equal to 0.6 * fctm [MPa].

        Returns
        -------
        MPA
            Example: 1.7378808922901334 (for C30/37)
        """
        return self.f_ctm * 0.6

    @property
    def strain_cr(self) -> MPA:
        """Strain at crack tensile stress (long term) equal to sigma_cr / Ecm [MPa].

        Returns
        -------
        MPA
            Example: 5.2926083941105295e-05 (for C30/37)
        """
        return self.sigma_cr / self.e_cm

    @property
    def f_ctk_0_05(self) -> MPA:
        """Mean value of axial tensile strength of concrete, 5% fractile [MPa].

        Returns
        -------
        MPA
            Example: 2.027527707671822 (for C30/37)
        """
        return self.f_ctm * 0.7

    @property
    def f_ctd(self) -> MPA:
        """Design value of tensile strength of concrete [MPa].

        Returns
        -------
        MPA
        Example: 1.3516851384478814 (for C30/37)
        """
        return self.f_ctk_0_05 / 1.5

    @property
    def f_ctk_0_95(self) -> MPA:
        """Mean value of axial tensile strength of concrete, 95% fractile [MPa].

        Returns
        -------
        MPA
            Example: 3.765408599961956 (for C30/37)
        """
        return self.f_ctm * 1.3

    @property
    def e_cm(self) -> MPA:
        """Secant modulus of elasticity of concrete [MPa].

        Returns
        -------
        MPA
            Example: 32836 (for C30/37)
        """
        return int(22 * ((self.f_cm / 10) ** 0.3) * GPA_TO_MPA)

    @property
    def custom_e_c_present(self) -> bool:
        """Checks if the value of Ec equal is to the value from table 3.1 of NEN-EN 1992-1-1.

        Returns
        -------
        bool
            Example: False if ConcreteMaterial.e_cm is equal to 32836 (for C30/37)
        """
        if self.e_c == self.e_cm:
            return False
        return True

    @property
    def eps_c1(self) -> PER_MILLE:
        """Compressive strain in the concrete_checks at the peak stress fc [‰ (per mille)]. Value with a maximum of 2.8 ‰.
        Check Figure 3.2 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 2.1618768697354804 (for C30/37)
        """
        return min(0.7 * self.f_cm**0.31, 2.8)

    @property
    def eps_cu1(self) -> PER_MILLE:
        """Nominal ultimate compressive strain in the concrete_checks [‰ (per mille)]. Check Figure 3.2 of NEN-EN 1992-1-1.

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
        """Compressive strain at reaching the maximum strength according to Table 3.1 [‰ (per mille)]. Check Figure 3.3 of NEN-EN 1992-1-1.

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
        """Nominal ultimate compressive strain in the concrete_checks according to Table 3.1 [‰ (per mille)]. Check Figure 3.3 of NEN-EN 1992-1-1.

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
        """N factor from table 3.1 of NEN-EN 1992-1-1 [-].

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
        """Compressive strain at reaching the maximum strength according to a Bi-linear stress-strain relation [‰ (per mille)].

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
        """Nominal ultimate compressive strain in the concrete_checks according to a Bi-linear stress-strain relation [‰ (per mille)].

        Check Figure 3.4 of NEN-EN 1992-1-1.

        Returns
        -------
        PER_MILLE
            Example: 3.5 (for C30/37)
        """
        if self.f_ck >= 50:
            return 2.6 + 35 * ((90 - self.f_ck) / 100) ** 4
        return 3.5

    @property
    def cement_class(self) -> CementClass:
        """Cement class needed for calculation of Creep and shrinkage strain (Annex B from NEN-EN 1992-1-1). Classes are S, N and R.

        Returns
        -------
        CementClass
            Example: "N" (standard value)
        """
        return self._cement_class

    @property
    def density(self) -> KG:
        """Unit mass of concrete [kg/m3].

        Returns
        -------
        KG
            Example: 2500.0 (for regular reinforced concrete)
        """
        return self._density

    @property
    def diagram_type(self) -> DiagramType:
        """Type of stress-strain diagram (Figures 3.2, 3.3 and 3.4 from NEN-EN 1992-1-1).

        Returns
        -------
        DiagramType
            Example: DiagramType.BI-LINEAR
        """
        return self._diagram_type

    @property
    def aggregate_type(self) -> ConcreteAggregateType:
        """Type of aggregate in the concrete material (NEN-EN 1992-1-1).

        Returns
        -------
        ConcreteAggregateType
            Example: "Kwartsiet" (standard value)
        """
        return self._aggregate_type

    @property
    def aggregate_size(self) -> MM:
        """Largest nominal maximum aggregate size [mm] (NEN-EN 1992-1-1).

        Returns
        -------
        MM
            Example: 16.0 (standard value)
        """
        return self._aggregate_size

    @property
    def plain_concrete_diagram(self) -> bool:
        """Use a Stress-strain diagram for plain or lightly reinforced concrete (NEN-EN 1992-1-1). (True or False).

        Returns
        -------
        bool
            Example: False (standard value)
        """
        return self._plain_concrete_diagram

    def rho_min(self, f_yd: MPA) -> PERCENTAGE:
        """Minimum reinforcement ratio (CB2, 7de druk 2011, pag.55) [%].

        Parameters
        ----------
        f_yd: MPA
            Design yield strength of reinforcement [MPa]

        Returns
        -------
        PERCENTAGE
        """
        return (0.223 * (self.f_ctm / f_yd)) * 100

    @property
    def cement_type(self) -> CementType:
        """Type of cement in the concrete material (NEN-EN 1992-1-1).

        Returns
        -------
        CementType
            Example: CementType.CEM_I
        """
        return self._cement_type

    def __eq__(self, other: object) -> bool:
        """Check if two ConcreteMaterial objects are equal."""
        if not isinstance(other, ConcreteMaterial):
            raise NotImplementedError
        properties_self = {
            attribute: self.__getattribute__(attribute)
            for attribute in dir(self)
            if not attribute.startswith("_") and attribute not in ["id", "name", "rho_min"]
        }
        properties_other = {
            attribute: other.__getattribute__(attribute)
            for attribute in dir(self)
            if not attribute.startswith("_") and attribute not in ["id", "name", "rho_min"]
        }
        return properties_self == properties_other
