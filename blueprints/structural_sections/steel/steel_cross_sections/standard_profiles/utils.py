"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from typing import Concatenate


class AsCrossSection[S, **P, R]:
    """Descriptor to convert a function into an instance method that auto-passes the instance."""

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

        def bound(*args: P.args, **kwargs: P.kwargs) -> R:
            return self._func(obj, *args, **kwargs)

        return bound
