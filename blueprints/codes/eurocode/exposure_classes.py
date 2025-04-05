"""Module for the concrete exposure classes
according to Table 4.1 from NEN-EN 1992-1-1: Chapter 4 - Durability and cover to reinforcement.
"""

import re
from abc import abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Self

from blueprints.utils.abc_enum_meta import ABCEnumMeta


@total_ordering
class Exposure(Enum, metaclass=ABCEnumMeta):
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
        if not isinstance(other, self.__class__):
            raise TypeError("Only the same exposure class types can be compared with each other!")
        _self_severity = int(self.value[-1]) if self.value != "Not applicable" else 0
        _other_severity = int(other.value[-1]) if other.value != "Not applicable" else 0
        return _self_severity == _other_severity

    def __gt__(self, other: Self) -> bool:
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
    def options(cls) -> list[str]:
        """Return all the possible options within a subclass.

        Returns
        -------
        list[str]
            all the possible class designations within a specific exposure class
        """
        return [m._value_ for m in cls.__members__.values()]

    @staticmethod
    @abstractmethod
    def exposure_class_description() -> str:
        """Description of subclasses to be implemented in each subclass.

        Returns
        -------
        str
            description of the specific exposure class
        """

    @abstractmethod
    def description_of_the_environment(self) -> str:
        """Description of the environment based on the instance.

        Returns
        -------
        str
            description of the environment based on the instance
        """

    @classmethod
    def snake_case(cls) -> str:
        """Converts the name of a subclass to snake_case which can be used in a parametrization class.

        Returns
        -------
        str
            the name of a subclass in snake_case
        """
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()


@total_ordering
class CarbonationBase(Exposure):
    """Enum Class which indicates the classification of corrosion induced by carbonation."""


@total_ordering
class ChlorideBase(Exposure):
    """Enum Class which indicates the classification of corrosion induced by chlorides other than by sea water."""


@total_ordering
class ChlorideSeawaterBase(Exposure):
    """Enum Class which indicates the classification of corrosion induced by chlorides from sea water."""


@total_ordering
class FreezeThawBase(Exposure):
    """Enum Class which indicates the classification of freeze/thaw attack with or without de-icing agents."""


@total_ordering
class ChemicalBase(Exposure):
    """Enum Class which indicates the classification of chemical attack."""


@dataclass(frozen=True)
class ExposureClassesBase:
    """Parent class which serves as a container for the Exposure classes.

    Exposure classes related to environmental conditions in accordance with EN 206-1
    """

    carbonation: CarbonationBase
    chloride: ChlorideBase
    chloride_seawater: ChlorideSeawaterBase
    freeze: FreezeThawBase
    chemical: ChemicalBase

    @property
    def no_risk(self) -> bool:
        """Check if all exposure classes are 'Not applicable'.

        This represents X0 class designation according to table 4.1 from NEN-EN 1992-1-1+C2:2011.

        Returns
        -------
        bool
            True if all exposure classes are 'Not applicable'
        """
        return all(exposure_class.value == "Not applicable" for exposure_class in self.__dict__.values())

    def __str__(self) -> str:
        """String representation of the ExposureClasses object.

        Returns
        -------
        str
            String representation of the ExposureClasses object
        """
        return "X0" if self.no_risk else ", ".join(enum.value for enum in self.__dict__.values() if enum.value != "Not applicable")

    def __iter__(self) -> Iterator[Exposure]:
        """Iterator for the ExposureClasses object.

        Returns
        -------
        Iterable[Exposure]
            Iterator for the ExposureClasses object
        """
        return iter(self.__dict__.values())
