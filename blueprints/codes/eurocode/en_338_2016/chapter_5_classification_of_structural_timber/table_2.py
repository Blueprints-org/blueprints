"""Table 2 of EN 338:2016."""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from blueprints.codes.eurocode.en_338_2016 import EN_338_2016
from blueprints.type_alias import KG_M3, MPA
from blueprints.unit_conversion import GPA_TO_MPA


class SoftwoodStrengthClassTension(Enum):
    """Enumeration for softwood strength classes based on tension tests."""

    T8 = "T8"
    T9 = "T9"
    T10 = "T10"
    T11 = "T11"
    T12 = "T12"
    T13 = "T13"
    T14 = "T14"
    T14_5 = "T14.5"
    T15 = "T15"
    T16 = "T16"
    T18 = "T18"
    T21 = "T21"
    T22 = "T22"
    T24 = "T24"
    T26 = "T26"
    T27 = "T27"
    T28 = "T28"
    T30 = "T30"


@dataclass(frozen=True)
class Table2StrengthClassesSoftwoodTension:
    """Implementation of table 2 from EN 338:2016.

    Strength classes for softwood based on tension tests - strength, stiffness and density values.

    Parameters
    ----------
    timber_class : SoftwoodStrengthClassTension
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
    e_t_0_mean : MPA
        Mean characteristic value of modulus of elasticity in tension parallel to grain in N/mm²
    e_t_0_k : MPA
        5-percentile characteristic value of modulus of elasticity in tension parallel to grain in N/mm²
    e_t_90_mean : MPA
        Mean characteristic value of modulus of elasticity in tension perpendicular to grain in N/mm²
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
    >>> table = Table2StrengthClassesSoftwoodTension(SoftwoodStrengthClassTension.T14)
    >>> table.f_t_0_k
    14
    >>> table.e_t_0_mean
    11.0
    >>> table.rho_mean
    420
    """

    timber_class: SoftwoodStrengthClassTension
    label: str = field(init=False, default="Table 2")
    source_document: str = field(init=False, default=EN_338_2016)

    # Class variable containing all timber strength data
    # Format: {SoftwoodStrengthClassTension: (f_m_k, f_t_0_k, f_t_90_k, f_c_0_k, f_c_90_k, f_v_k,
    #                                        E_t_0_mean, E_t_0_k, E_t_90_mean, G_mean, rho_k, rho_mean)}
    _strength_data: ClassVar[dict[SoftwoodStrengthClassTension, tuple[float, ...]]] = {
        SoftwoodStrengthClassTension.T8: (13.5, 8, 0.4, 16, 2.0, 2.8, 7.0, 4.7, 0.23, 0.44, 290, 350),
        SoftwoodStrengthClassTension.T9: (14.5, 9, 0.4, 17, 2.1, 3.0, 7.5, 5.0, 0.25, 0.47, 300, 360),
        SoftwoodStrengthClassTension.T10: (16, 10, 0.4, 17, 2.2, 3.2, 8.0, 5.4, 0.27, 0.50, 310, 370),
        SoftwoodStrengthClassTension.T11: (17, 11, 0.4, 18, 2.2, 3.4, 9.0, 6.0, 0.30, 0.56, 320, 380),
        SoftwoodStrengthClassTension.T12: (18, 12, 0.4, 19, 2.3, 3.6, 9.5, 6.4, 0.32, 0.59, 330, 400),
        SoftwoodStrengthClassTension.T13: (19.5, 13, 0.4, 20, 2.4, 3.8, 10.0, 6.7, 0.33, 0.63, 340, 410),
        SoftwoodStrengthClassTension.T14: (20.5, 14, 0.4, 21, 2.5, 4.0, 11.0, 7.4, 0.37, 0.69, 350, 420),
        SoftwoodStrengthClassTension.T14_5: (21, 14.5, 0.4, 21, 2.5, 4.0, 11.0, 7.4, 0.37, 0.69, 350, 420),
        SoftwoodStrengthClassTension.T15: (22, 15, 0.4, 21, 2.5, 4.0, 11.5, 7.7, 0.38, 0.72, 360, 430),
        SoftwoodStrengthClassTension.T16: (23, 16, 0.4, 22, 2.6, 4.0, 11.5, 7.7, 0.38, 0.72, 370, 440),
        SoftwoodStrengthClassTension.T18: (25.5, 18, 0.4, 23, 2.7, 4.0, 12.0, 8.0, 0.40, 0.75, 380, 460),
        SoftwoodStrengthClassTension.T21: (29, 21, 0.4, 25, 2.7, 4.0, 13.0, 8.7, 0.43, 0.81, 390, 470),
        SoftwoodStrengthClassTension.T22: (30.5, 22, 0.4, 26, 2.7, 4.0, 13.0, 8.7, 0.43, 0.81, 390, 470),
        SoftwoodStrengthClassTension.T24: (33, 24, 0.4, 27, 2.8, 4.0, 13.5, 9.0, 0.45, 0.84, 400, 480),
        SoftwoodStrengthClassTension.T26: (35, 26, 0.4, 28, 2.9, 4.0, 14.0, 9.4, 0.47, 0.88, 410, 490),
        SoftwoodStrengthClassTension.T27: (36.5, 27, 0.4, 29, 2.9, 4.0, 15.0, 10.1, 0.50, 0.94, 410, 490),
        SoftwoodStrengthClassTension.T28: (37.5, 28, 0.4, 29, 2.9, 4.0, 15.0, 10.1, 0.50, 0.94, 420, 500),
        SoftwoodStrengthClassTension.T30: (40, 30, 0.4, 30, 3.0, 4.0, 15.5, 10.4, 0.52, 0.97, 430, 520),
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
            valid_classes = ", ".join([cls.name for cls in SoftwoodStrengthClassTension])
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
    def e_t_0_mean(self) -> MPA:
        """
        Get the mean characteristic value of modulus of elasticity in tension parallel to grain.

        Returns
        -------
        MPA
            The mean characteristic value of modulus of elasticity in tension parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][6] * GPA_TO_MPA

    @property
    def e_t_0_k(self) -> MPA:
        """
        Get the 5-percentile characteristic value of modulus of elasticity in tension parallel to grain.

        Returns
        -------
        MPA
            The 5-percentile characteristic value of modulus of elasticity in tension parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][7] * GPA_TO_MPA

    @property
    def e_t_90_mean(self) -> MPA:
        """
        Get the mean characteristic value of modulus of elasticity in tension perpendicular to grain.

        Returns
        -------
        MPA
            The mean characteristic value of modulus of elasticity in tension perpendicular to grain in N/mm²
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
        return f"{self.timber_class.value}, f_m,k={self.f_m_k} N/mm², E_0,mean={self.e_t_0_mean} N/mm², rho_mean={self.rho_mean} kg/m³"
