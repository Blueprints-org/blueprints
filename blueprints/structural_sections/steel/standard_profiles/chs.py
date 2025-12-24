"""Standard CHS profiles."""

from __future__ import annotations

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.standard_profiles.chs_dict import CHS_PROFILES


class ProfileDescriptor:
    """Descriptor for standard profiles.

    This descriptor allows accessing standard profiles as class attributes
    that return profile instances initialized with data from the database.

    Attributes
    ----------
    profile_key : str
        The key to look up in the profile database.
    """

    def __init__(self) -> None:
        """Initialize the descriptor.

        The profile key will be set automatically when assigned to a class attribute.
        """
        print("Initializing ProfileDescriptor")
        self.profile_key: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        """Capture the attribute name when the descriptor is assigned to a class.

        Parameters
        ----------
        owner : type
            The class owning the descriptor.
        name : str
            The name of the attribute (e.g., "CHS21_3x2_3").
        """
        print(f"Setting profile descriptor name: {name}")
        self.profile_key = name

    def __get__(self, obj: CHS, objtype: type[CHS] | None = None) -> CHSProfile:
        """Return a profile instance when the descriptor is accessed.

        Parameters
        ----------
        obj : Any
            The instance accessing the descriptor (None for class access).
        objtype : type[CHS] | None
            The class owning the descriptor.

        Returns
        -------
        CHSProfile
            A profile instance initialized with data from the database.
        """
        print("Accessing standard profile:", self.profile_key)
        if objtype is None:
            objtype = type(obj)

        # Get the profile data from the database
        profile_data = objtype._database[self.profile_key]

        # Create and return a profile instance with the data as kwargs
        return objtype._factory(**profile_data)


class CHS:
    """Geometrical representation of CHS profiles."""

    _database = CHS_PROFILES
    _factory = CHSProfile

    CHS21_3x2_3 = ProfileDescriptor()
    CHS26_3x2_9 = ProfileDescriptor()


if __name__ == "__main__":
    chs_profile = CHS.CHS21_3x2_3
    print(f"ID: {id(chs_profile)}")
    # another_chs_profile = CHS.CHS21_3x2_3
    # print(f"ID: {id(another_chs_profile)}")
    print(f"Profile Name: {chs_profile.name}")
