"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from typing import Concatenate, Generic, ParamSpec, TypeVar, cast

S = TypeVar("S")  # Type of the instance owning the descriptor
R = TypeVar("R")
P = ParamSpec("P")


class AsCrossSection(Generic[P, R]):  # noqa: UP046
    """Descriptor to convert a function into an instance method that auto-passes the instance."""

    def __init__(self, func: Callable[Concatenate[S, P], R]) -> None:
        """Initialize the descriptor with the class method to bind.

        Args
        ----
            func: The class method to be converted into an instance method.
        """
        self._func = func

    def __get__(self, obj: S, owner: type[S]) -> Callable[P, R]:
        """Bind the method to the instance.

        Args
        ----
            obj: The instance to bind the method to.
            owner: The class of the instance.

        Returns
        -------
            The bound method.

        Raises
        ------
            AttributeError: If accessed on the class rather than an instance.
        """
        if obj is None:
            raise AttributeError("Cannot access instance method on the class itself.")

        def bound(*args: P.args, **kwargs: P.kwargs) -> R:
            return self._func(obj, *args, **kwargs)  # type: ignore[arg-type]

        bound.__name__ = getattr(self._func, "__name__", self.__class__.__name__)

        return cast(Callable[P, R], bound)
