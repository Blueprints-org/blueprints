"""Custom metaclass for ABCEnum."""

from abc import ABCMeta
from enum import EnumMeta


class ABCEnumMeta(ABCMeta, EnumMeta):
    """Custom metaclass for ABCEnum.

    This metaclass is a combination of ABCMeta and EnumMeta.
    It is used to check if abstract methods are implemented in the class.
    """

    def __new__(cls, *args, **kwarg) -> type:
        """Create a new instance of the class.

        Here we check if the class has abstract methods that are not implemented.
        If so, we raise a TypeError.
        """
        abstract_enum_cls = super().__new__(cls, *args, **kwarg)
        # Only check abstractions if members were defined.
        if abstract_enum_cls._member_map_:
            try:  # Handle existence of undefined abstract methods.
                abstract_methods = list(abstract_enum_cls.__abstractmethods__)
                if abstract_methods:
                    missing = ", ".join(f"{method!r}" for method in abstract_methods)
                    plural = "s" if len(abstract_methods) > 1 else ""
                    raise TypeError(
                        f"Can't instantiate abstract class {abstract_enum_cls.__name__!r}"
                        f" without an implementation for abstract method{plural} {missing}"
                    )
            except AttributeError:
                pass
        return abstract_enum_cls
