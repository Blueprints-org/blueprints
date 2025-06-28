"""Module for the concrete exposure classes
according to Table 4.1 from EN 1992-1-1:2004: Chapter 4 - Durability and cover to reinforcement.
"""

from functools import total_ordering

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.exposure_classes import (
    Exposure,
    ExposureClassesBase,
)


@total_ordering
class Carbonation(Exposure):
    """Enum Class which indicates the classification of corrosion induced by carbonation."""

    NA = "Not applicable"
    XC1 = "XC1"
    XC2 = "XC2"
    XC3 = "XC3"
    XC4 = "XC4"

    @staticmethod
    def exposure_class_description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Corrosion induced by carbonation"

    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """
        match self:
            case Carbonation.XC1:
                return "Dry or permanently wet"
            case Carbonation.XC2:
                return "Wet, rarely dry"
            case Carbonation.XC3:
                return "Moderate humidity"
            case Carbonation.XC4:
                return "Cyclic wet and dry"
            case Carbonation.NA:
                return "Not applicable"


@total_ordering
class Chloride(Exposure):
    """Enum Class which indicates the classification of corrosion induced by chlorides other than by sea water."""

    NA = "Not applicable"
    XD1 = "XD1"
    XD2 = "XD2"
    XD3 = "XD3"

    @staticmethod
    def exposure_class_description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Corrosion induced by chlorides other than by sea water"

    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """
        match self:
            case Chloride.XD1:
                return "Moderate humidity"
            case Chloride.XD2:
                return "Wet, rarely dry"
            case Chloride.XD3:
                return "Cyclic wet and dry"
            case Chloride.NA:
                return "Not applicable"


@total_ordering
class ChlorideSeawater(Exposure):
    """Enum Class which indicates the classification of corrosion induced by chlorides from sea water."""

    NA = "Not applicable"
    XS1 = "XS1"
    XS2 = "XS2"
    XS3 = "XS3"

    @staticmethod
    def exposure_class_description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Corrosion induced by chlorides from sea water"

    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """
        match self:
            case ChlorideSeawater.XS1:
                return "Exposed to airborne salt but not in direct contact with sea water"
            case ChlorideSeawater.XS2:
                return "Permanently submerged"
            case ChlorideSeawater.XS3:
                return "Tidal, splash and spray zones"
            case ChlorideSeawater.NA:
                return "Not applicable"


@total_ordering
class FreezeThaw(Exposure):
    """Enum Class which indicates the classification of freeze/thaw attack with or without de-icing agents."""

    NA = "Not applicable"
    XF1 = "XF1"
    XF2 = "XF2"
    XF3 = "XF3"
    XF4 = "XF4"

    @staticmethod
    def exposure_class_description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Freeze/thaw attack with or without de-icing agents"

    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """
        match self:
            case FreezeThaw.XF1:
                return "Moderate water saturation, without de-icing agent"
            case FreezeThaw.XF2:
                return "Moderate water saturation, with de-icing agent"
            case FreezeThaw.XF3:
                return "High water saturation, without de-icing agents"
            case FreezeThaw.XF4:
                return "High water saturation with de-icing agents or sea water"
            case FreezeThaw.NA:
                return "Not applicable"


@total_ordering
class Chemical(Exposure):
    """Enum Class which indicates the classification of chemical attack."""

    NA = "Not applicable"
    XA1 = "XA1"
    XA2 = "XA2"
    XA3 = "XA3"

    @staticmethod
    def exposure_class_description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Chemical attack"

    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """
        match self:
            case Chemical.XA1:
                return "Slightly aggressive chemical environment according to EN 206-1, Table 2"
            case Chemical.XA2:
                return "Moderately aggressive chemical environment according to EN 206-1, Table 2"
            case Chemical.XA3:
                return "Highly aggressive chemical environment according to EN 206-1, Table 2"
            case Chemical.NA:
                return "Not applicable"


class Table4Dot1ExposureClasses(ExposureClassesBase):
    """Class representing table 4.1 from EN 1992-1-1:2004."""

    def __init__(
        self,
        carbonation: Carbonation = Carbonation.NA,
        chloride: Chloride = Chloride.NA,
        chloride_seawater: ChlorideSeawater = ChlorideSeawater.NA,
        freeze_thaw: FreezeThaw = FreezeThaw.NA,
        chemical: Chemical = Chemical.NA,
    ) -> None:
        """Implementation of table 4.1 from EN 1992-1-1:2004 par. 4.2.

        Exposure classes related to environmental conditions in accordance with EN 206-1

        Parameters
        ----------
        carbonation : Carbonation
            The carbonation exposure class. Defaults to Carbonation.NA.
        chloride : Chloride
            The chloride exposure class. Defaults to Chloride.NA.
        chloride_seawater : ChlorideSeawater
            The chloride seawater exposure class. Defaults to ChlorideSeawater.NA.
        freeze_thaw : FreezeThaw
            The freeze/thaw exposure class. Defaults to FreezeThaw.NA.
        chemical : Chemical
            The chemical exposure class. Defaults to Chemical.NA.
        """
        self.carbonation = carbonation
        self.chloride = chloride
        self.chloride_seawater = chloride_seawater
        self.freeze_thaw = freeze_thaw
        self.chemical = chemical
