"""Metaclass for Profile Enums.

This metaclass combines EnumMeta with the metaclass of Profile to ensure that standard profiles are both Enums and Profile instances.
"""

from __future__ import annotations

from enum import EnumMeta, FlagBoundary, _EnumDict

from blueprints.structural_sections._profile import Profile


class ProfileEnumMeta(EnumMeta, type(Profile)):  # type: ignore[misc]
    """Metaclass combining EnumMeta with Profile's metaclass.

    This metaclass handles the creation of enum members that are also Profile instances.
    It ensures proper initialization of both the Enum and dataclass aspects.
    """

    def __new__(
        mcs: type[ProfileEnumMeta],
        name: str,
        bases: tuple[type, ...],
        classdict: _EnumDict,
        boundary: FlagBoundary | None = None,
        _simple: bool = False,
        **kwds: object,
    ) -> type:
        """Create a new Profile Enum class.

        Parameters
        ----------
        mcs : type[ProfileEnumMeta]
            The metaclass itself.
        name : str
            The name of the class being created.
        bases : tuple[type, ...]
            The base classes of the class being created.
        classdict : _EnumDict
            The class dictionary containing class attributes and methods.
        boundary : FlagBoundary | None, optional
            The boundary condition for Flag enums, by default None.
        _simple : bool, optional
            Whether to create a simple enum, by default False.
        **kwds : object
            Additional keyword arguments.

        Returns
        -------
        type
            The newly created class.
        """
        # Let EnumMeta handle the class creation
        return super().__new__(mcs, name, bases, classdict, boundary=boundary, _simple=_simple, **kwds)
