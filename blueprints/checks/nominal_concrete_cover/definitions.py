"""Definitions for the nominal concrete cover check according to art. 4.4.1 (Concrete cover) from NEN-EN 1992-1-1+C2:2011."""

from enum import Enum


class AbrasionClass(Enum):
    """Enum representing the abrasion class of the concrete surface.

    According to art. 4.4.1.2 (13) from NEN-EN 1992-1-1+C2:2011
    """

    NA = "Not applicable"
    XM1 = "XM1"
    XM2 = "XM2"
    XM3 = "XM3"


class CastingSurface(Enum):
    """Enum representing the casting surface of the concrete.

    According to art. 4.4.1.3 (4) from NEN-EN 1992-1-1+C2:2011
    """

    PERMANENTLY_EXPOSED = "Permanently exposed"
    FORMWORK = "Formwork"
    PREPARED_GROUND = "Prepared ground (including blinding)"
    DIRECTLY_AGAINST_SOIL = "Directly against soil"
