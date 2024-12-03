"""Module for the concrete exposure classes
according to Table 4.1 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement.
"""

from collections.abc import Sequence
from functools import total_ordering
from typing import Self, TypeVar

from blueprints.codes.eurocode.exposure_classes import (
    CarbonationBase,
    ChemicalBase,
    ChlorideBase,
    ChlorideSeawaterBase,
    ExposureClassesBase,
    FreezeThawBase,
)


@total_ordering
class Carbonation(CarbonationBase):
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

    @staticmethod
    def notation() -> str:
        """Static method which returns the notation of this exposure class.

        Returns
        -------
        str
            notation of this exposure class
        """
        return "XC"


@total_ordering
class Chloride(ChlorideBase):
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

    @staticmethod
    def notation() -> str:
        """Static method which returns the notation of this exposure class.

        Returns
        -------
        str
            notation of this exposure class
        """
        return "XD"


@total_ordering
class ChlorideSeawater(ChlorideSeawaterBase):
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

    @staticmethod
    def notation() -> str:
        """Static method which returns the notation of this exposure class.

        Returns
        -------
        str
            notation of this exposure class
        """
        return "XS"


@total_ordering
class FreezeThaw(FreezeThawBase):
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

    @staticmethod
    def notation() -> str:
        """Static method which returns the notation of this exposure class.

        Returns
        -------
        str
            notation of this exposure class
        """
        return "XF"


@total_ordering
class Chemical(ChemicalBase):
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

    @staticmethod
    def notation() -> str:
        """Static method which returns the notation of this exposure class.

        Returns
        -------
        str
            notation of this exposure class
        """
        return "XA"


# Define a generic type for the class
T = TypeVar("T", bound="Table4Dot1ExposureClasses")


class Table4Dot1ExposureClasses(ExposureClassesBase):
    """Implementation of table 4.1 from NEN-EN 1992-1-1+C2:2011.

    Exposure classes related to environmental conditions in accordance with EN 206-1
    """

    carbonation: Carbonation
    chloride: Chloride
    chloride_seawater: ChlorideSeawater
    freeze: FreezeThaw
    chemical: Chemical

    @classmethod
    def from_exposure_list(cls, exposure_classes: Sequence[str]) -> Self:
        """Create an instance from a sequence of exposure classes.

        Examples
        --------
        >>> exposure_classes = ["XC1", "XD1", "XS1"]
        >>> Table4Dot1ExposureClasses().from_exposure_list(exposure_classes)
        Table4Dot1ExposureClasses(
            carbonation=<Carbonation.XC1: 'XC1'>,
            chloride=<Chloride.XD1: 'XD1'>,
            chloride_seawater=<ChlorideSeawater.XS1: 'XS1'>,
            freeze=<FreezeThaw.NA: 'Not applicable'>,
            chemical=<Chemical.NA: 'Not applicable'>
        )

        Parameters
        ----------
        exposure_classes : Sequence[str]
            list of exposure classes, order is not important. If an exposure class is not provided, it is set to "Not applicable"
            You can use capital letters or lowercase letters, the method is case-insensitive.
            For example, "XC1" and "xc1" are both valid.

        Returns
        -------
        Self
            instance created from the list
        """
        exposures: dict[str, Carbonation | Chloride | ChlorideSeawater | Chemical | FreezeThaw] = {}
        classifications = {
            classification.notation(): classification for classification in (Carbonation, Chloride, ChlorideSeawater, FreezeThaw, Chemical)
        }

        for exposure_str in exposure_classes:
            classification = classifications.get(exposure_str[:2].upper())
            if classification is None:
                raise ValueError(f"Invalid exposure class: '{exposure_str}'")
            classification_name = classification.snake_case().removesuffix("_thaw")
            if classification_name in exposures:
                raise ValueError(f"Duplication Error: There are multiple instances of '{classification.__name__}' class.")
            exposures[classification_name] = classification[exposure_str.upper()]

        for classification in classifications.values():
            classification_name = classification.snake_case().removesuffix("_thaw")
            if classification_name not in exposures:
                exposures.setdefault(classification_name, classification.NA)

        return cls(**exposures)  # type: ignore[arg-type]
