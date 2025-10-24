"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from functools import partial, update_wrapper
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
E = TypeVar("E", bound=Enum)


def wrap_function(func: Callable[Concatenate[E, P], R], self: E, /) -> Callable[P, R]:
    """Wrap a function to bind the Enum instance as the first argument."""
    bound = partial(func, self)
    update_wrapper(bound, func)
    return bound
