"""Table 1 of EN 338:2016."""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from blueprints.codes.eurocode.en_338_2016 import EN_338_2016
from blueprints.type_alias import KG_M3, MPA
from blueprints.unit_conversion import GPA_TO_MPA


class SoftwoodStrengthClassBending(Enum):
    """Enumeration for softwood strength classes based on edgewise bending tests."""

    C14 = "C14"
    C16 = "C16"
    C18 = "C18"
    C20 = "C20"
    C22 = "C22"
    C24 = "C24"
    C27 = "C27"
    C30 = "C30"
    C35 = "C35"
    C40 = "C40"
    C45 = "C45"
    C50 = "C50"


@dataclass(frozen=True)
class Table1StrengthClassesSoftwoodBending:
    """Implementation of table 1 from EN 338:2016.

    Strength classes for softwood based on edgewise bending tests - strength, stiffness and density values.

    Parameters
    ----------
    timber_class : SoftwoodStrengthClassBending
        The timber strength class according to EN 338:2016

    Properties
    ----------
    f_m_k : MPA
        5-percentile characteristic value of bending strength in N/mm²
    f_t_0_k : MPA
        5-percentile characteristic value of tensile strength parallel to grain in N/mm²
    f_t_90_k : MPA
        5-percentile characteristic value of tensile strength perpendicular to grain in N/mm²
    f_c_0_k : MPA
        5-percentile characteristic value of compressive strength parallel to grain in N/mm²
    f_c_90_k : MPA
        5-percentile characteristic value of compressive strength perpendicular to grain in N/mm²
    f_v_k : MPA
        5-percentile characteristic value of shear strength in N/mm²
    e_m_0_mean : MPA
        Mean characteristic value of modulus of elasticity in bending parallel to grain in N/mm²
    e_m_0_k : MPA
        5-percentile characteristic value of modulus of elasticity in bending parallel to grain in N/mm²
    e_m_90_mean : MPA
        Mean characteristic value of modulus of elasticity in bending perpendicular to grain in N/mm²
    g_mean : MPA
        Mean characteristic value of shear modulus in N/mm²
    rho_k : KG_M3
        5-percentile characteristic value of density in kg/m³
    rho_mean : KG_M3
        Mean characteristic value of density in kg/m³

    Raises
    ------
    ValueError
        If an invalid timber class is provided

    Examples
    --------
    >>> table = Table1StrengthClassesSoftwoodBending(SoftwoodStrengthClassBending.C24)
    >>> table.f_m_k
    24
    >>> table.e_m_0_mean
    11.0
    >>> table.rho_mean
    420
    """

    timber_class: SoftwoodStrengthClassBending
    label: str = field(init=False, default="Table 1")
    source_document: str = field(init=False, default=EN_338_2016)

    # Class variable containing all timber strength data
    # Format: {SoftwoodStrengthClassBending: (f_m_k, f_t_0_k, f_t_90_k, f_c_0_k, f_c_90_k, f_v_k,
    #                                 E_m_0_mean, E_m_0_k, E_m_90_mean, G_mean, rho_k, rho_mean)}
    _strength_data: ClassVar[dict[SoftwoodStrengthClassBending, tuple[float, ...]]] = {
        SoftwoodStrengthClassBending.C14: (14, 7.2, 0.4, 16, 2.0, 3.0, 7.0, 4.7, 0.23, 0.44, 290, 350),
        SoftwoodStrengthClassBending.C16: (16, 8.5, 0.4, 17, 2.2, 3.2, 8.0, 5.4, 0.27, 0.50, 310, 370),
        SoftwoodStrengthClassBending.C18: (18, 10, 0.4, 18, 2.2, 3.4, 9.0, 6.0, 0.30, 0.56, 320, 380),
        SoftwoodStrengthClassBending.C20: (20, 11.5, 0.4, 19, 2.3, 3.6, 9.5, 6.4, 0.32, 0.59, 330, 400),
        SoftwoodStrengthClassBending.C22: (22, 13, 0.4, 20, 2.4, 3.8, 10.0, 6.7, 0.33, 0.63, 340, 410),
        SoftwoodStrengthClassBending.C24: (24, 14.5, 0.4, 21, 2.5, 4.0, 11.0, 7.4, 0.37, 0.69, 350, 420),
        SoftwoodStrengthClassBending.C27: (27, 16.5, 0.4, 22, 2.5, 4.0, 11.5, 7.7, 0.38, 0.72, 360, 430),
        SoftwoodStrengthClassBending.C30: (30, 19, 0.4, 24, 2.7, 4.0, 12.0, 8.0, 0.40, 0.75, 380, 460),
        SoftwoodStrengthClassBending.C35: (35, 22.5, 0.4, 25, 2.7, 4.0, 13.0, 8.7, 0.43, 0.81, 390, 470),
        SoftwoodStrengthClassBending.C40: (40, 26, 0.4, 27, 2.8, 4.0, 14.0, 9.4, 0.47, 0.88, 400, 480),
        SoftwoodStrengthClassBending.C45: (45, 30, 0.4, 29, 2.9, 4.0, 15.0, 10.1, 0.50, 0.94, 410, 490),
        SoftwoodStrengthClassBending.C50: (50, 33.5, 0.4, 30, 3.0, 4.0, 16.0, 10.7, 0.53, 1.00, 430, 520),
    }

    def __post_init__(self) -> None:
        """
        Validate the input parameters after initialization.

        Raises
        ------
        ValueError
            If the timber class is not in the strength data dictionary
        """
        # Check if timber class is valid
        if self.timber_class not in self._strength_data:
            valid_classes = ", ".join([cls.name for cls in SoftwoodStrengthClassBending])
            error_msg = f"Invalid timber class: {self.timber_class}. Valid classes are: {valid_classes}"
            raise ValueError(error_msg)

    @property
    def f_m_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of bending strength.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of bending strength in N/mm²
        """
        return self._strength_data[self.timber_class][0]

    @property
    def f_t_0_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of tensile strength parallel to grain.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of tensile strength parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][1]

    @property
    def f_t_90_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of tensile strength perpendicular to grain.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of tensile strength perpendicular to grain in N/mm²
        """
        return self._strength_data[self.timber_class][2]

    @property
    def f_c_0_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of compressive strength parallel to grain.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of compressive strength parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][3]

    @property
    def f_c_90_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of compressive strength perpendicular to grain.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of compressive strength perpendicular to grain in N/mm²
        """
        return self._strength_data[self.timber_class][4]

    @property
    def f_v_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of shear strength.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of shear strength in N/mm²
        """
        return self._strength_data[self.timber_class][5]

    @property
    def e_m_0_mean(self) -> MPA:
        """
        Get the mean characteristic value of modulus of elasticity in bending parallel to grain.

        Returns
        -------
        MPA
            The mean characteristic value of modulus of elasticity in bending parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][6] * GPA_TO_MPA

    @property
    def e_m_0_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of modulus of elasticity in bending parallel to grain.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of modulus of elasticity in bending parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][7] * GPA_TO_MPA

    @property
    def e_m_90_mean(self) -> MPA:
        """
        Get the mean characteristic value of modulus of elasticity in bending perpendicular to grain.

        Returns
        -------
        MPA
            The mean characteristic value of modulus of elasticity in bending perpendicular to grain in N/mm²
        """
        return self._strength_data[self.timber_class][8] * GPA_TO_MPA

    @property
    def g_mean(self) -> MPA:
        """
        Get the mean characteristic value of shear modulus.

        Returns
        -------
        MPA
            The mean characteristic value of shear modulus in N/mm²
        """
        return self._strength_data[self.timber_class][9] * GPA_TO_MPA

    @property
    def rho_k(self) -> KG_M3:
        """
        Get the 5-percentile characteristic value of density.

        Returns
        -------
        KG_M3
            The 5-percentile characteristic value of density in kg/m³
        """
        return self._strength_data[self.timber_class][10]

    @property
    def rho_mean(self) -> KG_M3:
        """
        Get the mean characteristic value of density.

        Returns
        -------
        KG_M3
            The mean characteristic value of density in kg/m³
        """
        return self._strength_data[self.timber_class][11]

    def __str__(self) -> str:
        """
        Return a string representation of the hardwood properties.

        Returns
        -------
        str
            String representation with class and key strength properties
        """
        return f"{self.timber_class.value}, f_m,k={self.f_m_k} N/mm², E_0,mean={self.e_m_0_mean} N/mm², rho_mean={self.rho_mean} kg/m³"
