"""Utility functions and (meta)classes for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import NamedTuple, Protocol

from blueprints.structural_sections._profile import Profile


class StandardProfileProtocol(Protocol):
    """Protocol for standard profile classes."""

    _factory: Callable[..., Profile]
    """Factory class for creating standard profiles."""
    _database: dict[str, NamedTuple]
    """Database of standard profiles."""


class StandardProfileMeta(type):
    """Metaclass for standard profile classes to enable dynamic attribute access."""

    def __getattr__(cls: StandardProfileProtocol, name: str) -> Profile:
        """Get a profile by its name from the class database.

        Parameters
        ----------
        name : str
            The name of the profile to retrieve.

        Returns
        -------
        Profile
            An instance of the profile corresponding to the given name.

        Raises
        ------
        AttributeError
            If the profile name does not exist in the database.
        """
        try:
            profile = cls._database[name]
        except KeyError as e:
            raise AttributeError(f"Profile '{name}' does not exist in database.") from e
        return cls._factory(**profile._asdict())

    def __iter__(cls: StandardProfileProtocol) -> Iterator[Profile]:
        """Iterate over the profiles in the class database."""
        return (getattr(cls, profile_key) for profile_key in cls._database)
