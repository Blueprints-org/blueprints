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
        # Enum classes have a _member_map_ attribute that is a dictionary of the enum members.
        # If the class has abstract methods and the _member_map_ attribute is not empty, we check if the abstract methods are implemented.
        if getattr(abstract_enum_cls, "_member_map_", False) and getattr(abstract_enum_cls, "__abstractmethods__", False):
            abstract_methods = list(abstract_enum_cls.__abstractmethods__)
            missing = ", ".join(f"{method!r}" for method in abstract_methods)
            plural = "s" if len(abstract_methods) > 1 else ""
            raise TypeError(
                f"Can't instantiate abstract class {abstract_enum_cls.__name__!r} without an implementation for abstract method{plural} {missing}"
            )
        return abstract_enum_cls
