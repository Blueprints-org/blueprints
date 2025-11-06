"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Concatenate


def wrap_as_instance_method[S, T, R, **P](
    func: Callable[Concatenate[S, P], R],
) -> Callable[[Callable[[T], None]], Callable[Concatenate[S, P], R]]:
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

    def decorator(_instance_method: Callable[[T], None]) -> Callable[Concatenate[S, P], R]:
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
