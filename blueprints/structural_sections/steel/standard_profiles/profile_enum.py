"""Base Enum class for standard profiles that behave like Profile instances."""

from enum import Enum
from typing import Self

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import DEG, MM


class ProfileEnum(Enum):
    """Base Enum class for standard profiles that behave like Profile instances.

    This class allows enum members to be treated as instances of Profile subclasses.
    For this purpose, the new profile Enum classes should be defined as follows:

    ```python
    from blueprints.utils.abc_enum_meta import ABCEnumMeta
    from blueprints.structural_sections.steel.standard_profiles.profile_enum import ProfileEnum
    from blueprints.structural_sections.steel.profile_definitions.profile_subclass import ProfileSubClass  # Replace with actual subclass


    class StandardProfile(ProfileSubClass, ProfileEnum, metaclass=ABCEnumMeta):
        STANDARD_PROFILE_1 = ProfileSubClass(...)
        STANDARD_PROFILE_2 = ProfileSubClass(...)
        ...
    ```
    """

    def __new__(cls, profile: Profile) -> Self:
        """Override __new__ to create enum members as Profile instances with custom initialization and methods."""
        # Base profile class is always the first base class (This is how _get_mixins_ works in the enum module)
        base_profile_class = cls.__bases__[0]
        obj = base_profile_class.__new__(cls)  # type: ignore[call-overload]
        # _value_ attribute needs to be set in the __new__ method of the Enum
        obj._value_ = profile
        # __init__ method needs to be overridden, otherwise the base class __init__ will be called which expects different parameters
        obj.__init__ = ProfileEnum.__dict__["__init__"].__get__(obj, cls)
        # transform method needs to be overridden, otherwise the base class transform will be called which cannot handle the Enum instance
        obj.transform = ProfileEnum.__dict__["transform"].__get__(obj, cls)
        return obj

    def __init__(self, profile: Profile) -> None:
        """Initialize the enum member as a Profile subclass instance.

        This method extracts the fields from the provided Profile instance and
        initializes the Profile subclass instance with those fields.
        """
        base_profile_class: type[Profile] = self.__class__.__bases__[0]
        initializable_keys = {key for key, value in base_profile_class.__dataclass_fields__.items() if value.init}
        profile_dict = {key: value for key, value in profile.__dict__.items() if key in initializable_keys}
        base_profile_class.__init__(self, **profile_dict)  # type: ignore[arg-type]

    def transform(self, horizontal_offset: MM = 0, vertical_offset: MM = 0, rotation: DEG = 0) -> Self:
        """Specialized transform method for ProfileEnum. It returns a new profile with the applied transformations.

        Note
        ----
            Calling the base class transform method directly would lead to errors, since the base class expects a pure dataclass instance.
            If we called `super().transform(...)`, it would pass the Enum instance to the base class method, which is not compatible.
            This method uses the underlying Profile instance's transform method on the enum member's value.
            Enum member's value is a pure Profile instance, so we can call its transform method directly.

        Parameters
        ----------
        horizontal_offset : MM
            Horizontal offset to apply [mm]. Positive values move the centroid to the right.
        vertical_offset : MM
            Vertical offset to apply [mm]. Positive values move the centroid upwards.
        rotation : DEG
            Rotation to apply [degrees]. Positive values rotate counter-clockwise around the centroid.

        Returns
        -------
        Self
            New profile with the applied transformations.
        """
        return self.value.transform(horizontal_offset, vertical_offset, rotation)
