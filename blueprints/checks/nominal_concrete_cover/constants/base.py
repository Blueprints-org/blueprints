"""Base class for constants for the calculation of nominal concrete cover."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.type_alias import MM


@dataclass(frozen=True)
class NominalConcreteCoverConstantsBase(ABC):
    """Base class for constants for the calculation of nominal concrete cover."""

    COVER_INCREASE_FOR_UNEVEN_SURFACE: MM
    COVER_INCREATSE_FOR_ABRASION_CLASS: dict[AbrasionClass, MM]
    DEFAULT_DELTA_C_DEV: MM

    @staticmethod
    @abstractmethod
    def minimum_cover_with_regard_to_casting_surface(c_min_dur: MM, casting_surface: CastingSurface) -> MM:
        """Calculate the minimum cover with regard to casting surface according to art."""
