"""Standard Steel Strips."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.strip_profile import StripProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __StripProfileParameters(NamedTuple):
    """Parameters for defining a strip profile."""

    name: str
    """Name of the strip profile."""
    width: MM
    """Width of the strip profile."""
    height: MM
    """Height (thickness) of the strip profile."""


STRIP_PROFILES_DATABASE = {
    "STRIP160x5": __StripProfileParameters("160x5", 160, 5),
    "STRIP160x6": __StripProfileParameters("160x6", 160, 6),
    "STRIP160x8": __StripProfileParameters("160x8", 160, 8),
    "STRIP160x10": __StripProfileParameters("160x10", 160, 10),
    "STRIP160x12": __StripProfileParameters("160x12", 160, 12),
    "STRIP160x15": __StripProfileParameters("160x15", 160, 15),
    "STRIP160x20": __StripProfileParameters("160x20", 160, 20),
    "STRIP160x25": __StripProfileParameters("160x25", 160, 25),
    "STRIP160x30": __StripProfileParameters("160x30", 160, 30),
    "STRIP165x5": __StripProfileParameters("165x5", 165, 5),
    "STRIP165x6": __StripProfileParameters("165x6", 165, 6),
    "STRIP165x8": __StripProfileParameters("165x8", 165, 8),
    "STRIP165x10": __StripProfileParameters("165x10", 165, 10),
    "STRIP165x12": __StripProfileParameters("165x12", 165, 12),
    "STRIP165x15": __StripProfileParameters("165x15", 165, 15),
    "STRIP165x20": __StripProfileParameters("165x20", 165, 20),
    "STRIP165x25": __StripProfileParameters("165x25", 165, 25),
    "STRIP165x30": __StripProfileParameters("165x30", 165, 30),
    "STRIP170x5": __StripProfileParameters("170x5", 170, 5),
    "STRIP170x6": __StripProfileParameters("170x6", 170, 6),
    "STRIP170x8": __StripProfileParameters("170x8", 170, 8),
    "STRIP170x10": __StripProfileParameters("170x10", 170, 10),
    "STRIP170x12": __StripProfileParameters("170x12", 170, 12),
    "STRIP170x15": __StripProfileParameters("170x15", 170, 15),
    "STRIP170x20": __StripProfileParameters("170x20", 170, 20),
    "STRIP180x5": __StripProfileParameters("180x5", 180, 5),
    "STRIP180x6": __StripProfileParameters("180x6", 180, 6),
    "STRIP180x8": __StripProfileParameters("180x8", 180, 8),
    "STRIP180x10": __StripProfileParameters("180x10", 180, 10),
    "STRIP180x12": __StripProfileParameters("180x12", 180, 12),
    "STRIP180x15": __StripProfileParameters("180x15", 180, 15),
    "STRIP180x20": __StripProfileParameters("180x20", 180, 20),
    "STRIP180x25": __StripProfileParameters("180x25", 180, 25),
    "STRIP180x30": __StripProfileParameters("180x30", 180, 30),
    "STRIP180x40": __StripProfileParameters("180x40", 180, 40),
    "STRIP180x50": __StripProfileParameters("180x50", 180, 50),
    "STRIP200x5": __StripProfileParameters("200x5", 200, 5),
    "STRIP200x6": __StripProfileParameters("200x6", 200, 6),
    "STRIP200x8": __StripProfileParameters("200x8", 200, 8),
    "STRIP200x10": __StripProfileParameters("200x10", 200, 10),
    "STRIP200x12": __StripProfileParameters("200x12", 200, 12),
    "STRIP200x15": __StripProfileParameters("200x15", 200, 15),
    "STRIP200x20": __StripProfileParameters("200x20", 200, 20),
    "STRIP200x25": __StripProfileParameters("200x25", 200, 25),
    "STRIP200x30": __StripProfileParameters("200x30", 200, 30),
    "STRIP200x40": __StripProfileParameters("200x40", 200, 40),
    "STRIP200x50": __StripProfileParameters("200x50", 200, 50),
    "STRIP220x6": __StripProfileParameters("220x6", 220, 6),
    "STRIP220x8": __StripProfileParameters("220x8", 220, 8),
    "STRIP220x10": __StripProfileParameters("220x10", 220, 10),
    "STRIP220x12": __StripProfileParameters("220x12", 220, 12),
    "STRIP220x15": __StripProfileParameters("220x15", 220, 15),
    "STRIP220x20": __StripProfileParameters("220x20", 220, 20),
    "STRIP220x25": __StripProfileParameters("220x25", 220, 25),
    "STRIP220x30": __StripProfileParameters("220x30", 220, 30),
    "STRIP230x6": __StripProfileParameters("230x6", 230, 6),
    "STRIP230x8": __StripProfileParameters("230x8", 230, 8),
    "STRIP230x10": __StripProfileParameters("230x10", 230, 10),
    "STRIP230x12": __StripProfileParameters("230x12", 230, 12),
    "STRIP230x15": __StripProfileParameters("230x15", 230, 15),
    "STRIP230x20": __StripProfileParameters("230x20", 230, 20),
    "STRIP230x25": __StripProfileParameters("230x25", 230, 25),
}


class Strip(metaclass=StandardProfileMeta):
    """Geometrical representation of steel strips.

    This class provides access to standard strip profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a StripProfile instance.

    Usage example
    -------------
        >>> profile = Strip.STRIP200x10
        >>> print(isinstance(profile, StripProfile))  # True
        >>>
        >>> # To iterate over all available Strip profiles:
        >>> for profile in Strip:
        >>>     print(isinstance(profile, StripProfile))  # True
    """

    _factory = StripProfile
    """Factory class for creating standard strip profiles."""
    _database = STRIP_PROFILES_DATABASE
    """Database of standard strip profile parameters."""
