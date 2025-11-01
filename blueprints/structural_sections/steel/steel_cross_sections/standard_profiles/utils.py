"""Utility functions for standard steel cross-section profiles."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Concatenate


def wrap_as_instance_method[S, R, **P](
    func: Callable[Concatenate[S, P], R],
) -> Callable[[Callable[[S], None]], Callable[Concatenate[S, P], R]]:
    """Decorator to wrap a function into an instance method that auto-passes the instance.

    Type parameters
    ---------------
        S: self type. Equivalent to S = TypeVar('S') in older Python versions.
        R: return type. Equivalent to R = TypeVar('R') in older Python versions.
        P: parameter specification for args and kwargs. Equivalent to P = ParamSpec('P') in older Python versions.
        Callable is covariant in the return type, but contravariant in the arguments. This is automatically inferred by the type checker.
    """

    def decorator(instance_method: Callable[[S], None]) -> Callable[Concatenate[S, P], R]:  # noqa: ARG001
        @wraps(func)
        def wrapper(self: S, *args: P.args, **kwargs: P.kwargs) -> R:
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
