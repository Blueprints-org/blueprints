"""Table 3 of EN 338:2016."""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from blueprints.codes.eurocode.en_338_2016 import EN_338_2016
from blueprints.type_alias import KG_M3, MPA
from blueprints.unit_conversion import GPA_TO_MPA


class HardwoodStrengthClass(Enum):
    """Enumeration for hardwood strength classes based on edgewise bending tests."""

    D18 = "D18"
    D24 = "D24"
    D27 = "D27"
    D30 = "D30"
    D35 = "D35"
    D40 = "D40"
    D45 = "D45"
    D50 = "D50"
    D55 = "D55"
    D60 = "D60"
    D65 = "D65"
    D70 = "D70"
    D75 = "D75"
    D80 = "D80"


@dataclass(frozen=True)
class Table3StrengthClassesHardwoodBendingTests:
    """Implementation of table 3 from EN 338:2016.

    Strength classes for hardwoods based on edgewise bending tests - strength, stiffness and density values.

    Parameters
    ----------
    timber_class : HardwoodStrengthClass
        The hardwood strength class according to EN 338:2016

    Properties
    ----------
    f_m_k : MPA
        Characteristic bending strength in N/mm²
    f_t_0_k : MPA
        Characteristic tension strength parallel to grain in N/mm²
    f_t_90_k : MPA
        Characteristic tension strength perpendicular to grain in N/mm²
    f_c_0_k : MPA
        Characteristic compression strength parallel to grain in N/mm²
    f_c_90_k : MPA
        Characteristic compression strength perpendicular to grain in N/mm²
    f_v_k : MPA
        Characteristic shear strength in N/mm²
    e_m_0_mean : float
        Mean modulus of elasticity parallel to grain in kN/mm²
    e_m_0_k : float
        5 percentile modulus of elasticity parallel to grain in kN/mm²
    e_m_90_mean : float
        Mean modulus of elasticity perpendicular to grain in kN/mm²
    g_mean : float
        Mean shear modulus in kN/mm²
    rho_k : float
        5 percentile density in kg/m³
    rho_mean : float
        Mean density in kg/m³

    Raises
    ------
    ValueError
        If an invalid hardwood class is provided

    Examples
    --------
    >>> table = Table3StrengthClassesHardwoodBendingTests(HardwoodStrengthClass.D40)
    >>> table.f_m_k
    40
    >>> table.e_m_0_mean
    13.0
    >>> table.rho_mean
    660
    """

    timber_class: HardwoodStrengthClass
    label: str = field(init=False, default="Table 3")
    source_document: str = field(init=False, default=EN_338_2016)

    # Class variable containing all hardwood strength data
    # Format: {HardwoodStrengthClass: (f_m_k, f_t_0_k, f_t_90_k, f_c_0_k, f_c_90_k, f_v_k,
    #                                   E_m_0_mean, E_m_0_k, E_m_90_mean, G_mean, rho_k, rho_mean)}
    _strength_data: ClassVar[dict[HardwoodStrengthClass, tuple[float, ...]]] = {
        HardwoodStrengthClass.D18: (18, 11, 0.6, 18, 4.8, 3.5, 9.5, 8.0, 0.63, 0.59, 475, 570),
        HardwoodStrengthClass.D24: (24, 14, 0.6, 21, 4.9, 3.7, 10.0, 8.4, 0.67, 0.63, 485, 580),
        HardwoodStrengthClass.D27: (27, 16, 0.6, 22, 5.1, 3.8, 10.5, 8.8, 0.70, 0.66, 510, 610),
        HardwoodStrengthClass.D30: (30, 18, 0.6, 24, 5.3, 3.9, 11.0, 9.2, 0.73, 0.69, 530, 640),
        HardwoodStrengthClass.D35: (35, 21, 0.6, 25, 5.4, 4.1, 12.0, 10.1, 0.80, 0.75, 540, 650),
        HardwoodStrengthClass.D40: (40, 24, 0.6, 27, 5.5, 4.2, 13.0, 10.9, 0.87, 0.81, 550, 660),
        HardwoodStrengthClass.D45: (45, 27, 0.6, 29, 5.8, 4.4, 13.5, 11.3, 0.90, 0.84, 580, 700),
        HardwoodStrengthClass.D50: (50, 30, 0.6, 30, 6.2, 4.5, 14.0, 11.8, 0.93, 0.88, 620, 740),
        HardwoodStrengthClass.D55: (55, 33, 0.6, 32, 6.6, 4.7, 15.5, 13.0, 1.03, 0.97, 660, 790),
        HardwoodStrengthClass.D60: (60, 36, 0.6, 33, 10.5, 4.8, 17.0, 14.3, 1.13, 1.06, 700, 840),
        HardwoodStrengthClass.D65: (65, 39, 0.6, 35, 11.3, 5.0, 18.5, 15.5, 1.23, 1.16, 750, 900),
        HardwoodStrengthClass.D70: (70, 42, 0.6, 36, 12.0, 5.0, 20.0, 16.8, 1.33, 1.25, 800, 960),
        HardwoodStrengthClass.D75: (75, 45, 0.6, 37, 12.8, 5.0, 22.0, 18.5, 1.47, 1.38, 850, 1020),
        HardwoodStrengthClass.D80: (80, 48, 0.6, 38, 13.5, 5.0, 24.0, 20.2, 1.60, 1.50, 900, 1080),
    }

    def __post_init__(self) -> None:
        """
        Validate the input parameters after initialization.

        Raises
        ------
        ValueError
            If the hardwood class is not in the strength data dictionary
        """
        # Check if hardwood class is valid
        if self.timber_class not in self._strength_data:
            valid_classes = ", ".join([cls.name for cls in HardwoodStrengthClass])
            error_msg = f"Invalid hardwood class: {self.timber_class}. Valid classes are: {valid_classes}"
            raise ValueError(error_msg)

    @property
    def f_m_k(self) -> MPA:
        """
        Get the characteristic bending strength.

        Returns
        -------
        MPA
            The characteristic bending strength in N/mm²
        """
        return self._strength_data[self.timber_class][0]

    @property
    def f_t_0_k(self) -> MPA:
        """
        Get the characteristic tension strength parallel to grain.

        Returns
        -------
        MPA
            The characteristic tension strength parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][1]

    @property
    def f_t_90_k(self) -> MPA:
        """
        Get the characteristic tension strength perpendicular to grain.

        Returns
        -------
        MPA
            The characteristic tension strength perpendicular to grain in N/mm²
        """
        return self._strength_data[self.timber_class][2]

    @property
    def f_c_0_k(self) -> MPA:
        """
        Get the characteristic compression strength parallel to grain.

        Returns
        -------
        MPA
            The characteristic compression strength parallel to grain in N/mm²
        """
        return self._strength_data[self.timber_class][3]

    @property
    def f_c_90_k(self) -> MPA:
        """
        Get the characteristic compression strength perpendicular to grain.

        Returns
        -------
        MPA
            The characteristic compression strength perpendicular to grain in N/mm²
        """
        return self._strength_data[self.timber_class][4]

    @property
    def f_v_k(self) -> MPA:
        """
        Get the characteristic shear strength.

        Returns
        -------
        MPA
            The characteristic shear strength in N/mm²
        """
        return self._strength_data[self.timber_class][5]

    @property
    def e_m_0_mean(self) -> MPA:
        """
        Get the mean modulus of elasticity parallel to grain.

        Returns
        -------
        MPA
            The mean modulus of elasticity parallel to grain in kN/mm², multiplied by 1000 to convert from kN/mm² to N/mm²
        """
        return self._strength_data[self.timber_class][6] * GPA_TO_MPA

    @property
    def e_m_0_k(self) -> MPA:
        """
        Get the 5 percentile modulus of elasticity parallel to grain.

        Returns
        -------
        MPA
            The 5 percentile modulus of elasticity parallel to grain in kN/mm², multiplied by 1000 to convert from kN/mm² to N/mm²
        """
        return self._strength_data[self.timber_class][7] * GPA_TO_MPA

    @property
    def e_m_90_mean(self) -> MPA:
        """
        Get the mean modulus of elasticity perpendicular to grain.

        Returns
        -------
        MPA
            The mean modulus of elasticity perpendicular to grain in kN/mm², multiplied by 1000 to convert from kN/mm² to N/mm²
        """
        return self._strength_data[self.timber_class][8] * GPA_TO_MPA

    @property
    def g_mean(self) -> MPA:
        """
        Get the mean shear modulus.

        Returns
        -------
        MPA
            The mean shear modulus in kN/mm², multiplied by 1000 to convert from kN/mm² to N/mm²
        """
        return self._strength_data[self.timber_class][9] * GPA_TO_MPA

    @property
    def rho_k(self) -> KG_M3:
        """
        Get the 5 percentile density.

        Returns
        -------
        KG_M3
            The 5 percentile density in kg/m³
        """
        return self._strength_data[self.timber_class][10]

    @property
    def rho_mean(self) -> KG_M3:
        """
        Get the mean density.

        Returns
        -------
        KG_M3
            The mean density in kg/m³
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
