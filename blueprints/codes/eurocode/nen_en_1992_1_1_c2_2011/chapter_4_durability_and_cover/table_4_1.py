"""Module for the concrete exposure classes
according to Table 4.1 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement.
"""

from enum import Enum
from functools import total_ordering
from typing import NamedTuple, Type, TypeVar

T = TypeVar("T", bound="Exposure")


@total_ordering
class Exposure(Enum):
    """Parent class for individual exposure classes.

    This class handles the ordering/comparison operations, that's why it is decorated with total_ordering (As recommended by PEP8).
    On top of that, it handles a couple of methods which will be used by its subclasses.
    """

    def __eq__(self, other: object) -> bool:
        """Definition of '==' operator for the comparison of the severity of the exposure classifications.

        Parameters
        ----------
        self : Exposure/ subclass of Exposure
            First argument for the comparison.
        other : object
            Second argument for the comparison.

        Raises
        ------
        TypeError
            If different types are being compared.

        Returns
        -------
        Boolean
            True if both arguments are of the same severity (In this case they will both be literally the same).
        """
        if isinstance(other, self.__class__):
            _self_severity = int(self.value[-1]) if self.value != "Not applicable" else 0
            _other_severity = int(other.value[-1]) if other.value != "Not applicable" else 0
            return _self_severity == _other_severity
        raise TypeError("Only the same exposure class types can be compared with each other!")

    def __gt__(self, other: object) -> bool:
        """Definition of '>' operator for the comparison of the severity of the exposure classifications.

        Parameters
        ----------
        self : Exposure/ subclass of Exposure
            First argument for the comparison.
        other : object
            Second argument for the comparison.

        Raises
        ------
        TypeError
            If different types are being compared.

        Returns
        -------
        Boolean
            True if the first argument is more severe than the second argument.
        """
        if isinstance(other, self.__class__):
            _self_severity = int(self.value[-1]) if self.value != "Not applicable" else 0
            _other_severity = int(other.value[-1]) if other.value != "Not applicable" else 0
            return _self_severity > _other_severity
        raise TypeError("Only the same exposure class types can be compared with each other!")

    @classmethod
    def options(cls: Type[T]) -> list[str]:
        """Return all the possible options within a subclass.

        Returns
        -------
        list[str]
            all the possible class designations within a specific exposure class
        """
        return [m._value_ for m in cls.__members__.values()]

    @staticmethod
    def exposure_class_description() -> str:
        """Description of subclasses to be implemented in each subclass.

        Returns
        -------
        str
            description of the specific exposure class
        """
        raise NotImplementedError("The description method must be implemented in the subclass!")

    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """
        raise NotImplementedError("The description_of_the_environment method must be implemented in the subclass!")


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


class ExposureClasses(NamedTuple):
    """Implementation of tabel 4.1 from NEN-EN 1992-1-1+C2:2011.

    Exposure classes related to environmental conditions in accordance with EN 206-1
    """

    carbonation: Carbonation = Carbonation("Not applicable")
    chloride: Chloride = Chloride("Not applicable")
    chloride_seawater: ChlorideSeawater = ChlorideSeawater("Not applicable")
    freeze: FreezeThaw = FreezeThaw("Not applicable")
    chemical: Chemical = Chemical("Not applicable")

    def __str__(self) -> str:
        """String representation of the ExposureClasses object.

        Returns
        -------
        str
            String representation of the ExposureClasses object
        """
        if self.no_risk:
            return "X0"
        return ", ".join(enum.value for enum in self if enum.value != "Not applicable")

    @property
    def no_risk(self) -> bool:
        """Check if all exposure classes are 'Not applicable'.

        This represents X0 class designation according to table 4.1 from NEN-EN 1992-1-1+C2:2011.

        Returns
        -------
        bool
            True if all exposure classes are 'Not applicable'
        """
        return all(exposure_class.value == "Not applicable" for exposure_class in self)
