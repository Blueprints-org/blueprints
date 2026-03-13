"""Table 3.1 of EN 1993-1-1:2005."""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.type_alias import MM, MPA


class SteelStandardGroup(Enum):
    """Enumeration for steel standard groups in EN standards."""

    EN_10025_2 = "NEN-EN 10025-2"
    EN_10025_3 = "NEN-EN 10025-3"
    EN_10025_4 = "NEN-EN 10025-4"
    EN_10025_5 = "NEN-EN 10025-5"
    EN_10025_6 = "NEN-EN 10025-6"
    EN_10210_1 = "NEN-EN 10210-1"
    EN_10219_1 = "NEN-EN 10219-1"


class SteelStrengthClass(Enum):
    """Enumeration for steel strength classes with their standard group."""

    S235 = (SteelStandardGroup.EN_10025_2, "S 235")
    S275 = (SteelStandardGroup.EN_10025_2, "S 275")
    S355 = (SteelStandardGroup.EN_10025_2, "S 355")
    S450 = (SteelStandardGroup.EN_10025_2, "S 450")

    S275_N_NL_10025_3 = (SteelStandardGroup.EN_10025_3, "S 275 N/NL")
    S355_N_NL_10025_3 = (SteelStandardGroup.EN_10025_3, "S 355 N/NL")
    S420_N_NL_10025_3 = (SteelStandardGroup.EN_10025_3, "S 420 N/NL")
    S460_N_NL_10025_3 = (SteelStandardGroup.EN_10025_3, "S 460 N/NL")

    S275_M_ML_10025_4 = (SteelStandardGroup.EN_10025_4, "S 275 M/ML")
    S355_M_ML_10025_4 = (SteelStandardGroup.EN_10025_4, "S 355 M/ML")
    S420_M_ML_10025_4 = (SteelStandardGroup.EN_10025_4, "S 420 M/ML")
    S460_M_ML_10025_4 = (SteelStandardGroup.EN_10025_4, "S 460 M/ML")

    S235_W_10025_5 = (SteelStandardGroup.EN_10025_5, "S 235 W")
    S355_W_10025_5 = (SteelStandardGroup.EN_10025_5, "S 355 W")

    S460_Q_QL_QL1_10025_6 = (SteelStandardGroup.EN_10025_6, "S 460 Q/QL/QL1")

    S235_H_10210_1 = (SteelStandardGroup.EN_10210_1, "S 235 H")
    S275_H_10210_1 = (SteelStandardGroup.EN_10210_1, "S 275 H")
    S355_H_10210_1 = (SteelStandardGroup.EN_10210_1, "S 355 H")
    S275_NH_NLH_10210_1 = (SteelStandardGroup.EN_10210_1, "S 275 NH/NLH")
    S355_NH_NLH_10210_1 = (SteelStandardGroup.EN_10210_1, "S 355 NH/NLH")
    S420_NH_NLH_10210_1 = (SteelStandardGroup.EN_10210_1, "S 420 NH/NLH")
    S460_NH_NLH_10210_1 = (SteelStandardGroup.EN_10210_1, "S 460 NH/NLH")

    S235_H_10219_1 = (SteelStandardGroup.EN_10219_1, "S 235 H")
    S275_H_10219_1 = (SteelStandardGroup.EN_10219_1, "S 275 H")
    S355_H_10219_1 = (SteelStandardGroup.EN_10219_1, "S 355 H")
    S275_NH_NLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 275 NH/NLH")
    S355_NH_NLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 355 NH/NLH")
    S460_NH_NLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 460 NH/NLH")
    S275_MH_MLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 275 MH/MLH")
    S355_MH_MLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 355 MH/MLH")
    S420_MH_MLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 420 MH/MLH")
    S460_MH_MLH_10219_1 = (SteelStandardGroup.EN_10219_1, "S 460 MH/MLH")

    def __init__(self, standard_group: SteelStandardGroup, display_name: str) -> None:
        self.standard_group = standard_group
        self.display_name = display_name


@dataclass(frozen=True)
class Table3Dot1NominalValuesHotRolledStructuralSteel:
    """Implementation of table 3.1 from EN 1993-1-1:2005.

    Nominal values for yield strength (fy) and ultimate tensile strength (fu) for hot-rolled structural steel.

    Parameters
    ----------
    steel_class : SteelStrengthClass
        The steel strength class according to EN standards
    thickness : MM
        The nominal thickness of the steel element in mm

    Methods
    -------
    fy : MPA
        Returns the yield strength in N/mm². In the case of EN 10219-1, the values are not specified
        for thickness > 40 mm and will return None.
    fu : MPA
        Returns the ultimate tensile strength in N/mm². In the case of EN 10219-1, the values are not specified
        for thickness > 40 mm and will return None.

    Raises
    ------
    ValueError
        If an invalid steel class is provided
        If the thickness is not a positive number

    Examples
    --------
    >>> table = Table3Dot1NominalValuesHotRolledStructuralSteel(SteelStrengthClass.EN_10025_2_S355, 30)
    >>> table.fy
    355
    >>> table.fu
    490
    """

    steel_class: SteelStrengthClass
    thickness: MM
    label: str = field(init=False, default="Table 3.1")
    source_document: str = field(init=False, default=EN_1993_1_1_2005)

    # Class variable containing all strength data
    # Format: {SteelStrengthClass: (fy_t≤40, fu_t≤40, fy_t>40, fu_t>40)}
    _strength_data: ClassVar[dict[SteelStrengthClass, tuple[int, int, int | None, int | None]]] = {
        # EN 10025-2
        SteelStrengthClass.S235: (235, 360, 215, 360),
        SteelStrengthClass.S275: (275, 430, 255, 410),
        SteelStrengthClass.S355: (355, 490, 335, 470),
        SteelStrengthClass.S450: (440, 550, 410, 550),
        # EN 10025-3
        SteelStrengthClass.S275_N_NL_10025_3: (275, 390, 255, 370),
        SteelStrengthClass.S355_N_NL_10025_3: (355, 490, 335, 470),
        SteelStrengthClass.S420_N_NL_10025_3: (420, 520, 390, 520),
        SteelStrengthClass.S460_N_NL_10025_3: (460, 540, 430, 540),
        # EN 10025-4
        SteelStrengthClass.S275_M_ML_10025_4: (275, 370, 255, 360),
        SteelStrengthClass.S355_M_ML_10025_4: (355, 470, 335, 450),
        SteelStrengthClass.S420_M_ML_10025_4: (420, 520, 390, 500),
        SteelStrengthClass.S460_M_ML_10025_4: (460, 540, 430, 530),
        # EN 10025-5
        SteelStrengthClass.S235_W_10025_5: (235, 360, 215, 340),
        SteelStrengthClass.S355_W_10025_5: (355, 490, 335, 490),
        # EN 10025-6
        SteelStrengthClass.S460_Q_QL_QL1_10025_6: (460, 570, 440, 550),
        # EN 10210-1
        SteelStrengthClass.S235_H_10210_1: (235, 360, 215, 340),
        SteelStrengthClass.S275_H_10210_1: (275, 430, 255, 410),
        SteelStrengthClass.S355_H_10210_1: (355, 510, 335, 490),
        SteelStrengthClass.S275_NH_NLH_10210_1: (275, 390, 255, 370),
        SteelStrengthClass.S355_NH_NLH_10210_1: (355, 490, 335, 470),
        SteelStrengthClass.S420_NH_NLH_10210_1: (420, 540, 390, 520),
        SteelStrengthClass.S460_NH_NLH_10210_1: (460, 560, 430, 550),
        # EN 10219-1
        SteelStrengthClass.S235_H_10219_1: (235, 360, None, None),
        SteelStrengthClass.S275_H_10219_1: (275, 430, None, None),
        SteelStrengthClass.S355_H_10219_1: (355, 510, None, None),
        SteelStrengthClass.S275_NH_NLH_10219_1: (275, 370, None, None),
        SteelStrengthClass.S355_NH_NLH_10219_1: (355, 470, None, None),
        SteelStrengthClass.S460_NH_NLH_10219_1: (460, 550, None, None),
        SteelStrengthClass.S275_MH_MLH_10219_1: (275, 360, None, None),
        SteelStrengthClass.S355_MH_MLH_10219_1: (355, 470, None, None),
        SteelStrengthClass.S420_MH_MLH_10219_1: (420, 500, None, None),
        SteelStrengthClass.S460_MH_MLH_10219_1: (460, 530, None, None),
    }

    def __post_init__(self) -> None:
        """
        Validate the input parameters after initialization.

        Raises
        ------
        ValueError
            If the steel class is not in the strength data dictionary
            If the thickness is not a positive number
        """
        # Check if steel class is valid
        if self.steel_class not in self._strength_data:
            valid_classes = ", ".join([cls.name for cls in SteelStrengthClass])
            error_msg = f"Invalid steel class: {self.steel_class}. Valid classes are: {valid_classes}"
            raise ValueError(error_msg)

        # Check if thickness is positive
        if not isinstance(self.thickness, int | float) or self.thickness <= 0:
            raise ValueError(f"Thickness must be a positive number, got {self.thickness}")

    @property
    def fy(self) -> MPA:
        """
        Get the yield strength (fy) for the steel class and thickness.

        Returns
        -------
        MPA
            The yield strength in N/mm²

        Raises
        ------
        ValueError
            If the thickness is greater than 80 mm
        """
        # Check if thickness is within valid range (≤80 mm)
        if self.thickness > 80:
            raise ValueError(f"Thickness {self.thickness} mm exceeds maximum supported value of 80 mm")

        strength_values = self._strength_data[self.steel_class]

        # Choose value based on thickness (≤40 mm or >40 mm and ≤80 mm)
        result = strength_values[0] if self.thickness <= 40 else strength_values[2]

        if result is None:
            raise ValueError(
                f"Yield strength not specified for thickness > 40 mm for steel class '{self.steel_class.value}'. "
                f"Check {self.label} from {self.source_document}."
            )

        return result

    @property
    def fu(self) -> MPA:
        """
        Get the ultimate tensile strength (fu) for the steel class and thickness.

        Returns
        -------
        MPA
            The ultimate tensile strength in N/mm²

        Raises
        ------
        ValueError
            If the thickness is greater than 80 mm
        """
        # Check if thickness is within valid range (≤80 mm)
        if self.thickness > 80:
            raise ValueError(f"Thickness {self.thickness} mm exceeds maximum supported value of 80 mm")

        strength_values = self._strength_data[self.steel_class]

        # Choose value based on thickness (≤40 mm or >40 mm and ≤80 mm)
        result = strength_values[1] if self.thickness <= 40 else strength_values[3]

        if result is None:
            raise ValueError(
                f"Yield strength not specified for thickness > 40 mm for steel class '{self.steel_class.value}'. "
                f"Check {self.label} from {self.source_document}."
            )

        return result

    def __str__(self) -> str:
        """
        Return a string representation of the steel properties.

        Returns
        -------
        str
            String representation with class, thickness, and strength properties
        """
        return f"{self.steel_class.display_name}, t={round(self.thickness, 1)} mm, fy={round(self.fy, 2)} N/mm², fu={round(self.fu, 2)} N/mm²"
