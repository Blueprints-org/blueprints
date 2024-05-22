"""Module for the concrete exposure classes."""

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
    def description() -> str:
        """Description of subclasses to be implemented in each subclass.

        Returns
        -------
        str
            description of the specific exposure class
        """
        return "Not implemented"


@total_ordering
class Carbonation(Exposure):
    """Enum Class which indicates the classification of corrosion induced by carbonation."""

    NA = "Not applicable"
    XC1 = "XC1"
    XC2 = "XC2"
    XC3 = "XC3"
    XC4 = "XC4"

    @staticmethod
    def description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Corrosion induced by carbonation"


@total_ordering
class Chloride(Exposure):
    """Enum Class which indicates the classification of corrosion induced by chlorides other than by sea water."""

    NA = "Not applicable"
    XD1 = "XD1"
    XD2 = "XD2"
    XD3 = "XD3"

    @staticmethod
    def description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Corrosion induced by chlorides other than by sea water"


@total_ordering
class ChlorideSeawater(Exposure):
    """Enum Class which indicates the classification of corrosion induced by chlorides from sea water."""

    NA = "Not applicable"
    XS1 = "XS1"
    XS2 = "XS2"
    XS3 = "XS3"

    @staticmethod
    def description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Corrosion induced by chlorides from sea water"


@total_ordering
class Freeze(Exposure):
    """Enum Class which indicates the classification of freeze/thaw attack with or without de-icing agents."""

    NA = "Not applicable"
    XF1 = "XF1"
    XF2 = "XF2"
    XF3 = "XF3"
    XF4 = "XF4"

    @staticmethod
    def description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Freeze/thaw attack with or without de-icing agents"


@total_ordering
class Chemical(Exposure):
    """Enum Class which indicates the classification of chemical attack."""

    NA = "Not applicable"
    XA1 = "XA1"
    XA2 = "XA2"
    XA3 = "XA3"

    @staticmethod
    def description() -> str:
        """Static method which returns the description of this exposure class.

        Returns
        -------
        str
            description of this exposure class
        """
        return "Chemical attack"


class ExposureClasses(NamedTuple):
    """Named tuple, collects all the different exposure classes of a surface."""

    carbonation: Carbonation = Carbonation("Not applicable")
    chloride: Chloride = Chloride("Not applicable")
    chloride_seawater: ChlorideSeawater = ChlorideSeawater("Not applicable")
    freeze: Freeze = Freeze("Not applicable")
    chemical: Chemical = Chemical("Not applicable")

    def __str__(self) -> str:
        """String representation of the ExposureClasses object.

        Returns
        -------
        str
            String representation of the ExposureClasses object
        """
        return ", ".join(
            enum.value
            for enum in self
            if enum.value != "Not applicable"  # pylint: disable=not-an-iterable
        )
