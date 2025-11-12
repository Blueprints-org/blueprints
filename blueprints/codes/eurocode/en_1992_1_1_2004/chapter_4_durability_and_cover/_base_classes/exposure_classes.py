"""Module for the concrete exposure classes
according to Table 4.1 from EN 1992-1-1: Chapter 4 - Durability and cover to reinforcement.
"""

import re
from abc import abstractmethod
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import ClassVar, Self

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

    def __hash__(self) -> int:
        """Return hash value for the Exposure instance.

        The hash is based on the class type and the severity level to ensure
        consistency with the __eq__ method.

        Returns
        -------
        int
            Hash value for the instance
        """
        severity = int(self.value[-1]) if self.value != "Not applicable" else 0
        return hash((self.__class__, severity))

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

    @classmethod
    def notation(cls) -> str:
        """Returns the notation of the exposure class.

        Returns
        -------
        str
            notation of the exposure class, e.g. "XC", "XD", etc.
        """
        options = cls.options()
        # Look for this pattern in the options: Uppercase letters followed by at least one digit
        # If the pattern is found, return the Uppercase letters part
        for option in options:
            match = re.match(r"([A-Z]+)(\d+)", option)
            if match:
                return match.group(1)
        raise ValueError(
            f"No valid notation found for {cls.__name__}.\n"
            "Either adhere to the pattern of Uppercase letters followed by at least one digit for Enum values, "
            "or implement the notation method in the subclass."
        )


@dataclass(frozen=True)
class ExposureClassesBase:
    """Parent class which serves as a container for the Exposure classes.

    Exposure classes related to environmental conditions in accordance with EN 206-1
    """

    _not_applicable_key: ClassVar[str] = "Not applicable"
    """Key for the 'Not applicable' exposure class. Can be overridden in subclasses if needed."""

    @property
    def no_risk(self) -> bool:
        """Check if all exposure classes are 'Not applicable' (specified by _not_applicable_key).

        This represents X0 class designation according to table 4.1 from EN 1992-1-1:2004.

        Returns
        -------
        bool
            True if all exposure classes are euqal to _not_applicable_key ("Not applicable" by default)
        """
        return all(exposure_class.value == self.__class__._not_applicable_key for exposure_class in self.__dict__.values())  # noqa: SLF001

    def __str__(self) -> str:
        """String representation of the ExposureClasses object.

        Returns
        -------
        str
            String representation of the ExposureClasses object
        """
        return "X0" if self.no_risk else ", ".join(enum.value for enum in self.__dict__.values() if enum.value != self.__class__._not_applicable_key)  # noqa: SLF001

    def __iter__(self) -> Iterator[Exposure]:
        """Iterator for the ExposureClasses object.

        Returns
        -------
        Iterator[Exposure]
            Iterator for the ExposureClasses object
        """
        return iter(self.__dict__.values())

    @classmethod
    def from_exposure_list(cls, exposure_classes: Sequence[str]) -> Self:
        """Create an instance from a sequence of exposure classes.

        Examples
        --------
        >>> exposure_classes = ["XC1", "XD1", "XS1"]
        >>> ConcreteExposureClasses().from_exposure_list(exposure_classes)
        ConcreteExposureClasses(
            carbonation=<Carbonation.XC1: 'XC1'>,
            chloride=<Chloride.XD1: 'XD1'>,
            chloride_seawater=<ChlorideSeawater.XS1: 'XS1'>,
            freeze_thaw=<FreezeThaw.NA: 'Not applicable'>,
            chemical=<Chemical.NA: 'Not applicable'>
        )

        Parameters
        ----------
        exposure_classes : Sequence[str]
            sequence of exposure classes, order is not important.
            If an exposure class is not provided, but is defined in the __init__, it is set to the value of _not_applicable_key ("Not applicable").
            You can use capital letters or lowercase letters, the method is case-insensitive.
            For example, "XC1" and "xc1" are both valid.

        Returns
        -------
        Self
            instance created from the list
        """
        exposures: dict[str, Exposure] = {}
        classifications: dict[str, type[Exposure]] = {arg.notation(): arg for kw, arg in cls.__init__.__annotations__.items() if kw != "return"}

        for exposure_str in exposure_classes:
            classification = classifications.get(exposure_str[:2].upper())
            if classification is None:
                raise ValueError(f"Invalid exposure class: '{exposure_str}'")
            classification_name = classification.snake_case()
            if classification_name in exposures:
                raise ValueError(f"Duplication Error: There are multiple instances of '{classification.__name__}' class.")
            exposures[classification_name] = classification[exposure_str.upper()]

        for classification in classifications.values():
            classification_name = classification.snake_case()
            if classification_name not in exposures:
                exposures.setdefault(classification_name, classification(cls._not_applicable_key))

        return cls(**exposures)
