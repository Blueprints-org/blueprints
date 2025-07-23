"""Definitions and base classes for constants for the calculation of nominal concrete cover according to art. 4.4.1 from EN 1992-1-1:2004."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from blueprints.type_alias import MM


class AbrasionClass(Enum):
    """Enum representing the abrasion class of the concrete surface.

    According to art. 4.4.1.2 (13) from EN 1992-1-1:2004
    """

    NA = "Not applicable"
    XM1 = "XM1"
    XM2 = "XM2"
    XM3 = "XM3"


class CastingSurface(Enum):
    """Enum representing the casting surface of the concrete.

    According to art. 4.4.1.3 (4) from EN 1992-1-1:2004
    """

    PERMANENTLY_EXPOSED = "Permanently exposed"
    FORMWORK = "Formwork"
    PREPARED_GROUND = "Prepared ground (including blinding)"
    DIRECTLY_AGAINST_SOIL = "Directly against soil"


@dataclass(frozen=True)
class NominalConcreteCoverConstantsBase(ABC):
    """Base class for constants for the calculation of nominal concrete cover."""

    CODE_PREFIX: str  # Prefix for the code representing the country, e.g. "NEN-, DIN-, BS-, etc."
    CODE_SUFFIX: str  # Suffix for the code representing the publication year, e.g. "+C2:2011"
    COVER_INCREASE_FOR_UNEVEN_SURFACE: MM
    COVER_INCREASE_FOR_ABRASION_CLASS: dict[AbrasionClass, MM]
    DEFAULT_DELTA_C_DEV: MM

    @staticmethod
    @abstractmethod
    def minimum_cover_with_regard_to_casting_surface(c_min_dur: MM, casting_surface: CastingSurface) -> MM:
        """Calculate the minimum cover with regard to casting surface according to art. 4.4.1.3 (4) from EN 1992-1-1."""

    @staticmethod
    @abstractmethod
    def minimum_cover_with_regard_to_casting_surface_latex(casting_surface: CastingSurface) -> str:
        """LateX representation of minimum cover with regard to casting surface according to art. 4.4.1.3 (4) from EN 1992-1-1."""
