"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Concatenate, Protocol

from blueprints.structural_sections._profile import Profile


def wrap_as_instance_method[S, R, **P](
    func: Callable[Concatenate[S, P], R],
) -> Callable[[Callable[[S], None]], Callable[Concatenate[S, P], R]]:
    """Decorator to wrap a function into an instance method that auto-passes the instance.

    Type parameters
    ---------------
        S: self type. Equivalent to S = TypeVar('S') in older Python versions.
        P: parameter specification for args and kwargs. Equivalent to P = ParamSpec('P') in older Python versions.
        R: return type. Equivalent to R = TypeVar('R') in older Python versions.
        Callable is covariant in the return type, but contravariant in the arguments. This is automatically inferred by the type checker.

    Parameters
    ----------
    func : Callable[Concatenate[S, P], R]
        The function to be converted into an instance method.

    """

    def decorator(_instance_method: Callable[[S], None]) -> Callable[Concatenate[S, P], R]:
        """Decorator that passes the wrapped function as an instance method.

        Parameters
        ----------
        instance_method : Callable[[S], None]
            The instance method that acts as a placeholder for the wrapped function.
        """

        @wraps(func)
        def wrapper(self: S, *args: P.args, **kwargs: P.kwargs) -> R:
            """Wrapper function that calls the original function with the instance as the first argument."""
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class StandardProfile(Protocol):
    """Protocol for standard profile classes."""

    _factory: Callable[..., Profile]
    _database: dict[str, tuple[str | int | float, ...]]
    _parameters: tuple[str, ...]


class StandardProfileMeta(type):
    """Metaclass for standard profile classes to enable dynamic attribute access."""

    def __getattr__(cls: StandardProfile, name: str) -> Profile:
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
        return cls._factory(**dict(zip(cls._parameters, profile)))
