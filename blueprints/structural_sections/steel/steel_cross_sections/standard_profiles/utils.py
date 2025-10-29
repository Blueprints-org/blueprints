"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from typing import Concatenate


# It is intentionally chosen for a specific descriptor name rather than a generic one:
# 1) because the name shows up in the IDE as part of the method signature, making it clearer what the method does
# 2) because descriptors are an advanced topic and can lead to unexpected behaviors if not used carefully
class AsCrossSection[S, **P, R]:
    """Non-data descriptor to convert a function into an instance method that auto-passes the instance.

    Type parameters
    ---------------
        S: self type. Equivalent to S = TypeVar('S') in older Python versions.
        P: parameter specification for args and kwargs. Equivalent to P = ParamSpec('P') in older Python versions.
        R: return type. Equivalent to R = TypeVar('R') in older Python versions.
        Callable is covariant in the return type, but contravariant in the arguments. This is automatically inferred by the type checker.
    """

    def __init__(self, func: Callable[Concatenate[S, P], R]) -> None:
        """Initialize the descriptor with the function to bind.

        Parameters
        ----------
        func : Callable[Concatenate[S, P], R]
            The function to be converted into an instance method.
        """
        self._func = func

    def __get__(self, obj: S, owner: type[S]) -> Callable[P, R]:
        """Bind the method to the instance.

        This method allows the function to be called as an instance method, automatically passing the instance as the first argument.
        The function signature is preserved, allowing for additional arguments and keyword arguments in the future.

        Parameters
        ----------
        obj : S
            The instance to bind the method to.
        owner : type[S]
            The class of the instance.

        Returns
        -------
        Callable[P, R]
            The bound method.

        Raises
        ------
        AttributeError
            If accessed on the class rather than an instance.
        """
        if obj is None:
            raise AttributeError("Cannot access instance method on the class itself.")

        # By defining an inner function in this way, we preserve the signature of the original function.
        def bound(*args: P.args, **kwargs: P.kwargs) -> R:
            return self._func(obj, *args, **kwargs)

        return bound
